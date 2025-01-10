// src/utils/date.js

/**
 * 格式化日期为 YYYY-MM-DD 格式
 * @param {Date|string|number} date 要格式化的日期对象、日期字符串或时间戳
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(date) {
  try {
    const dateObj = new Date(date);
    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const day = String(dateObj.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  } catch (error) {
    console.error('日期格式化失败:', error);
    return ''; // 返回空字符串或根据需要返回其他默认值
  }
}

// 你可以根据需要添加其他的日期格式化函数，例如：

/**
 * 格式化日期时间为 YYYY-MM-DD HH:mm:ss 格式
 * @param {Date|string|number} date 要格式化的日期对象、日期字符串或时间戳
 * @returns {string} 格式化后的日期时间字符串
 */
export function formatDateTime(date) {
  try {
    const dateObj = new Date(date);
    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const day = String(dateObj.getDate()).padStart(2, '0');
    const hour = String(dateObj.getHours()).padStart(2, '0');
    const minute = String(dateObj.getMinutes()).padStart(2, '0');
    const second = String(dateObj.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
  } catch (error) {
    console.error('日期时间格式化失败:', error);
    return '';
  }
}

/**
 * 获取相对日期，例如：今天、昨天、前天
 * @param {Date|string|number} date 要比较的日期
 * @returns {string} 相对日期字符串
 */
export function getRelativeDate(date) {
  try {
    const dateObj = new Date(date);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);
    const twoDaysAgo = new Date(today);
    twoDaysAgo.setDate(today.getDate() - 2);

    const formattedDate = formatDate(dateObj);
    const formattedToday = formatDate(today);
    const formattedYesterday = formatDate(yesterday);
    const formattedTwoDaysAgo = formatDate(twoDaysAgo);

    if (formattedDate === formattedToday) {
      return '今天';
    } else if (formattedDate === formattedYesterday) {
      return '昨天';
    } else if (formattedDate === formattedTwoDaysAgo) {
      return '前天';
    } else {
      return formattedDate;
    }
  } catch (error) {
    console.error('获取相对日期失败:', error);
    return formatDate(date); // 失败时返回原始格式化日期
  }
}
