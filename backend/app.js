const express = require('express');
const maintenanceRoutes = require('./routes/maintenanceRoutes');

const app = express();

// 注册API路由
app.use('/api/maintenance', maintenanceRoutes); 