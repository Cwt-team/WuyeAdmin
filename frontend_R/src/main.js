// main.js
import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import App from './App.vue';
import router from './router';
import './assets/css/global.css'; // 引入全局CSS样式

const app = createApp(App);

app.use(router);
app.use(ElementPlus);

app.mount('#app'); 