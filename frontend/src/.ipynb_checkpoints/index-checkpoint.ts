import jQuery from 'jquery';

// @ts-ignore
window.jQuery = window.$ = jQuery;
import 'semantic-ui-css/semantic';
// import 'semantic-ui-css/components/popup';


import Vue from 'vue';

// @ts-ignore
import App from './templates/App.vue';

let app = new Vue({
  el: '#app',
  render: h => h(App),
});
