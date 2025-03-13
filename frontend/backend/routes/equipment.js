const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const pool = require('../db');

// ... 保留现有路由 ...

// 检查设备网络状态
router.post('/:id/check-network', async (req, res) => {
    try {
        const equipmentId = req.params.id;

        // 获取设备信息
        const [rows] = await pool.query('SELECT * FROM equipment WHERE id = ?', [equipmentId]);

        if (rows.length === 0) {
            return res.status(404).json({ message: '设备不存在' });
        }

        const equipment = rows[0];

        if (!equipment.ip) {
            return res.status(400).json({ message: '设备没有IP地址' });
        }

        // 使用ping命令检测网络连接
        const pingCommand = process.platform === 'win32'
            ? `ping -n 1 ${equipment.ip}`
            : `ping -c 1 ${equipment.ip}`;

        exec(pingCommand, async (error, stdout, stderr) => {
            const now = new Date();
            let networkStatus = 'unknown';

            if (!error) {
                networkStatus = 'online';
            } else {
                networkStatus = 'offline';
            }

            // 获取当前网络状态
            const [currentStatus] = await pool.query(
                'SELECT networkStatus FROM equipment WHERE id = ?',
                [equipmentId]
            );

            const previousStatus = currentStatus[0]?.networkStatus || 'unknown';

            // 更新数据库
            await pool.query(
                'UPDATE equipment SET networkStatus = ?, lastNetworkCheckTime = ? WHERE id = ?',
                [networkStatus, now, equipmentId]
            );

            // 如果状态发生变化，记录到历史表
            if (previousStatus !== networkStatus) {
                await pool.query(
                    'INSERT INTO equipment_status_history (equipmentId, previousStatus, newStatus, changeTime) VALUES (?, ?, ?, ?)',
                    [equipment.equipmentId, `network_${previousStatus}`, `network_${networkStatus}`, now]
                );
            }

            res.json({
                id: equipmentId,
                networkStatus,
                lastNetworkCheckTime: now
            });
        });
    } catch (error) {
        console.error('检查设备网络状态失败:', error);
        res.status(500).json({ message: '检查设备网络状态失败' });
    }
});

module.exports = router; 