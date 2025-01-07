// main.js
import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import App from './App.vue';
import router from './router';
import axios from 'axios';

const app = createApp(App);

// 配置 Axios
axios.defaults.baseURL = 'http://localhost:5000'; // 根据实际情况修改
axios.defaults.withCredentials = true; // 允许携带 Cookie

app.config.globalProperties.$axios = axios; // 可选：将 Axios 挂载到全局属性

app.use(router);
app.use(ElementPlus);

app.mount('#app');
