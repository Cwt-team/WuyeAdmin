const express = require('express');
const dgram = require('dgram');
const cors = require('cors'); // 引入 cors 中间件
const app = express();
const port = 3000;
const { promisify } = require('util');
const mysql = require('mysql2/promise');

// 创建 UDP 客户端
const udpClient = dgram.createSocket('udp4');

// 创建数据库连接池
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'wuye_admin',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// 解析 JSON 请求体
app.use(express.json());

// 使用 cors 中间件
app.use(cors());

// 在 server.js 中实现异步心跳检测
const sendAsync = promisify(udpClient.send.bind(udpClient));

// HTTP 接口：接收前端心跳包请求
app.post('/api/sendHeartbeat', (req, res) => {
  const heartbeatData = req.body;

  // 将数据转换为 JSON 字符串
  const message = JSON.stringify(heartbeatData);

  // 目标设备地址
  const deviceIp = '192.168.1.49';  // 替换为设备 IP
  const devicePort = 7998;       // 替换为设备端口

  // 发送 UDP 数据包
  udpClient.send(message, devicePort, deviceIp, (err) => {
    if (err) {
      console.error('发送 UDP 数据包失败:', err);
      res.status(500).json({
        result: "1",  // 失败状态码
        message: "心跳发送失败",
        cmd: "heartack"
      });
    } else {
      console.log('发送 UDP 数据包成功:', message);
      res.json({
        result: "0",  // 成功状态码
        message: "心跳发送成功",
        cmd: "heartack"
      });
    }
  });
});

// 发送心跳包到所有设备
app.post('/api/sendHeartbeat/all', async (req, res) => {
  try {
    // 从数据库获取所有设备
    const [rows] = await pool.execute('SELECT ip, port, communityCode, uid FROM equipment WHERE ip IS NOT NULL AND ip != ""');

    let successCount = 0;
    let failCount = 0;

    // 为每个设备发送心跳包
    for (const device of rows) {
      if (!device.ip) continue;

      try {
        const message = JSON.stringify({
          cmd: "heart",
          communityId: device.communityCode || '000000',
          deviceCode: device.uid || '000000'
        });

        // 使用 Promise 包装 UDP 发送
        await new Promise((resolve, reject) => {
          udpClient.send(message, device.port || 7998, device.ip, (err) => {
            if (err) reject(err);
            else resolve();
          });
        });

        successCount++;
      } catch (error) {
        console.error(`发送心跳包到设备 ${device.equipmentName} 失败:`, error);
        failCount++;
      }
    }

    res.json({
      result: "0",
      message: `心跳包发送完成: ${successCount}个成功, ${failCount}个失败`,
      cmd: "heartack"
    });
  } catch (error) {
    console.error('发送心跳包失败:', error);
    res.status(500).json({
      result: "1",
      message: "心跳发送失败: " + error.message,
      cmd: "heartack"
    });
  }
});

// 发送心跳包到特定设备
app.post('/api/sendHeartbeat/device', (req, res) => {
  const { deviceIp, devicePort, communityCode, uid } = req.body;

  if (!deviceIp) {
    return res.status(400).json({
      result: "1",
      message: "缺少设备IP地址",
      cmd: "heartack"
    });
  }

  const message = JSON.stringify({
    cmd: "heart",
    communityId: communityCode || '000000',
    deviceCode: uid || '000000'
  });

  udpClient.send(message, devicePort || 7998, deviceIp, (err) => {
    if (err) {
      console.error('发送UDP数据包失败:', err);
      res.status(500).json({
        result: "1",
        message: "心跳发送失败: " + err.message,
        cmd: "heartack"
      });
    } else {
      console.log('发送UDP数据包成功:', message);

      // 更新设备最后心跳时间
      pool.execute('UPDATE equipment SET lastHeartbeatTime = ? WHERE ip = ?', [new Date(), deviceIp]).then(result => {
        if (result.affectedRows > 0) {
          console.log(`设备 ${deviceIp} 状态已更新为在线`);
        } else {
          console.log(`未找到IP为 ${deviceIp} 的设备`);
        }
      }).catch(err => {
        console.error('更新设备心跳时间失败:', err);
      });

      res.json({
        result: "0",
        message: "心跳发送成功",
        cmd: "heartack"
      });
    }
  });
});

// 获取特定设备的状态
app.get('/api/equipment/:id/status', async (req, res) => {
  try {
    const deviceId = req.params.id;
    const [rows] = await pool.execute('SELECT status, lastResponseTime, lastStatusTime FROM equipment WHERE equipmentId = ?', [deviceId]);

    if (rows.length === 0) {
      return res.status(404).json({ message: "设备不存在" });
    }

    const device = rows[0];

    // 检查设备最后心跳响应时间，如果在5分钟内有响应，则认为在线
    const lastResponseTime = device.lastResponseTime || null;
    const now = new Date();
    const fiveMinutesAgo = new Date(now.getTime() - 5 * 60 * 1000);

    const status = lastResponseTime && new Date(lastResponseTime) > fiveMinutesAgo ? 'online' : 'offline';

    res.json({
      id: device.equipmentId,
      status: status,
      lastStatusTime: device.lastStatusTime || null
    });
  } catch (error) {
    console.error('获取设备状态失败:', error);
    res.status(500).json({ message: "获取设备状态失败: " + error.message });
  }
});

// 监听设备响应
udpClient.on('message', (msg, rinfo) => {
  console.log(`收到来自 ${rinfo.address}:${rinfo.port} 的消息: ${msg}`);

  try {
    const response = JSON.parse(msg.toString());

    // 如果是心跳响应
    if (response.cmd === "heartack") {
      // 更新设备状态为在线
      pool.execute('UPDATE equipment SET status = ?, lastResponseTime = ?, lastStatusTime = ? WHERE ip = ?', [
        'online',
        new Date(),
        new Date(),
        rinfo.address
      ]).then(result => {
        if (result.affectedRows > 0) {
          console.log(`设备 ${rinfo.address} 状态已更新为在线`);
        } else {
          console.log(`未找到IP为 ${rinfo.address} 的设备`);
        }
      }).catch(err => {
        console.error('更新设备状态失败:', err);
      });
    }
  } catch (error) {
    console.error('解析设备响应失败:', error);
  }
});

// 每5分钟检查一次所有设备状态
setInterval(async () => {
  try {
    console.log('开始检查设备状态...');

    // 获取所有设备
    const [rows] = await pool.execute('SELECT equipmentId, ip, port, communityCode FROM equipment WHERE ip IS NOT NULL AND ip != ""');

    // 当前时间
    const now = new Date();
    const tenMinutesAgo = new Date(now.getTime() - 10 * 60 * 1000);

    // 更新所有设备状态
    for (const device of rows) {
      // 如果最后响应时间超过10分钟，则标记为离线
      const lastResponseTime = device.lastResponseTime ? new Date(device.lastResponseTime) : null;
      const status = lastResponseTime && lastResponseTime > tenMinutesAgo ? 'online' : 'offline';

      // 只有状态变化时才更新
      if (device.status !== status) {
        await pool.execute('UPDATE equipment SET status = ?, lastStatusTime = ? WHERE equipmentId = ?', [
          status,
          now,
          device.equipmentId
        ]);
        console.log(`设备 ${device.equipmentName} (${device.ip}) 状态已更新为 ${status}`);
      }
    }

    console.log('设备状态检查完成');
  } catch (error) {
    console.error('检查设备状态失败:', error);
  }
}, 5 * 60 * 1000); // 5分钟

// 在 server.js 中实现异步心跳检测
app.post('/api/sendHeartbeatAsync/device', async (req, res) => {
  const { deviceIp, devicePort, communityCode, uid } = req.body;

  if (!deviceIp) {
    return res.status(400).json({
      result: "1",
      message: "缺少设备IP地址",
      cmd: "heartack"
    });
  }

  const message = JSON.stringify({
    cmd: "heart",
    communityId: communityCode || '000000',
    deviceCode: uid || '000000'
  });

  // 立即返回响应，不等待设备回复
  res.json({
    result: "0",
    message: "心跳包已发送，正在等待设备响应",
    cmd: "heartack"
  });

  try {
    // 异步发送心跳包
    await sendAsync(message, devicePort || 7998, deviceIp);
    console.log(`心跳包已发送到 ${deviceIp}:${devicePort}`);

    // 更新设备最后心跳时间
    await pool.execute('UPDATE equipment SET lastHeartbeatTime = ? WHERE ip = ?', [new Date(), deviceIp]);
  } catch (error) {
    console.error(`发送心跳包到 ${deviceIp}:${devicePort} 失败:`, error);
  }
});

// 获取设备状态
app.get('/api/equipment/status', async (req, res) => {
  try {
    const { equipmentId } = req.query;

    // 如果提供了设备ID，则查询特定设备
    if (equipmentId) {
      const [rows] = await pool.execute(
        'SELECT equipmentId, status, lastStatusTime FROM equipment WHERE equipmentId = ?',
        [equipmentId]
      );

      if (rows.length === 0) {
        return res.status(404).json({ message: "设备不存在" });
      }

      return res.json(rows[0]);
    }

    // 否则返回所有设备的状态
    const [rows] = await pool.execute(
      'SELECT equipmentId, equipmentName, ip, status, lastStatusTime FROM equipment'
    );

    res.json(rows);
  } catch (error) {
    console.error('获取设备状态失败:', error);
    res.status(500).json({ message: "获取设备状态失败: " + error.message });
  }
});

// 获取设备状态历史记录
app.get('/api/equipment/:equipmentId/status/history', async (req, res) => {
  try {
    const { equipmentId } = req.params;
    const limit = parseInt(req.query.limit) || 10;

    const [rows] = await pool.execute(
      'SELECT * FROM equipment_status_history WHERE equipmentId = ? ORDER BY changeTime DESC LIMIT ?',
      [equipmentId, limit]
    );

    res.json(rows);
  } catch (error) {
    console.error('获取设备状态历史失败:', error);
    res.status(500).json({ message: "获取设备状态历史失败: " + error.message });
  }
});

// 手动检查设备状态
app.post('/api/equipment/:equipmentId/check-status', async (req, res) => {
  try {
    const { equipmentId } = req.params;

    // 获取设备信息
    const [devices] = await pool.execute(
      'SELECT * FROM equipment WHERE equipmentId = ?',
      [equipmentId]
    );

    if (devices.length === 0) {
      return res.status(404).json({ message: "设备不存在" });
    }

    const device = devices[0];

    if (!device.ip) {
      return res.status(400).json({ message: "设备没有IP地址" });
    }

    // 发送UDP心跳包检查状态
    const udpClient = require('dgram').createSocket('udp4');

    const message = JSON.stringify({
      cmd: "heart",
      communityId: device.communityCode || '000000',
      deviceCode: device.equipmentId
    });

    let statusResult = 'offline';

    // 使用Promise包装UDP通信
    try {
      await new Promise((resolve, reject) => {
        // 设置超时
        const timeout = setTimeout(() => {
          udpClient.close();
          reject(new Error("请求超时"));
        }, 3000);

        // 监听响应
        udpClient.on('message', (msg, rinfo) => {
          clearTimeout(timeout);

          try {
            const response = JSON.parse(msg.toString());
            if (response.cmd === "heartack" && response.result === "0") {
              statusResult = 'online';
            }
            resolve();
          } catch (e) {
            reject(e);
          }
        });

        // 发送请求
        udpClient.send(message, device.port || 7998, device.ip, (err) => {
          if (err) {
            clearTimeout(timeout);
            reject(err);
          }
        });
      });
    } catch (error) {
      console.log(`设备 ${equipmentId} 状态检查失败: ${error.message}`);
      // 失败时状态默认为离线
    } finally {
      udpClient.close();
    }

    // 更新设备状态
    const now = new Date();

    // 获取当前状态
    const [currentStatusRows] = await pool.execute(
      'SELECT status FROM equipment WHERE equipmentId = ?',
      [equipmentId]
    );

    const previousStatus = currentStatusRows[0]?.status;

    // 更新设备状态
    await pool.execute(
      'UPDATE equipment SET status = ?, lastStatusTime = ? WHERE equipmentId = ?',
      [statusResult, now, equipmentId]
    );

    // 如果状态与之前不同，记录历史
    if (previousStatus !== statusResult) {
      await pool.execute(
        'INSERT INTO equipment_status_history (equipmentId, previousStatus, newStatus, changeTime) VALUES (?, ?, ?, ?)',
        [equipmentId, previousStatus, statusResult, now]
      );
    }

    res.json({
      equipmentId,
      status: statusResult,
      lastStatusTime: now
    });
  } catch (error) {
    console.error('检查设备状态失败:', error);
    res.status(500).json({ message: "检查设备状态失败: " + error.message });
  }
});

// 启动 HTTP 服务器
app.listen(port, () => {
  console.log(`HTTP 服务器运行在 http://localhost:${port}`);
});