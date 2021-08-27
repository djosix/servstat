import '/node_modules/fomantic-ui-css/semantic.min.css';

import { createApp } from 'vue';
import App from './App.vue';

const app = createApp(App);

app.config.globalProperties.$filters = {
  formatSize(n, maxUnit, precision, pad = ' ', keep = 3, comma = false) {
    const units = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'];
    let p = 2 ** 10;
    let finalUnit;
    let afterPrec = false;
    for (let unit of units) {
      if (precision === unit) {
        n = Math.round(n);
        afterPrec = true;
      }
      finalUnit = unit;
      if (n < p) {
        break;
      } else if (unit === maxUnit) {
        break;
      } else if (unit === 'Y') {
        break;
      }
      n /= p;
    }
    if (!afterPrec) {
      n = Math.round(n);
    }
    let k = 10 ** keep;
    n = Math.round(k * n) / k;
    if (comma) {
      n = n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    }
    return `${n}${pad}${finalUnit}`;
  }
}

app.mount('#app');
