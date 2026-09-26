# visual-web

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## 调用百度智能云模型所遇问题
1、搭建后端服务，调用ernie-4.5-turbo-32k模型

2、调试接口路径，开始路径不正确，参数报错，根据提示解决

3、重点问题：代码里

```ts
const response = await chatToApi.openAiDoor({ messages: messages.value })

if(response.ok) throw new Error(`HTTP ${response.status}`)

const reader = response.body!.getReader()

```

openAiDoor之前我写的时候用的是axios封装接口，到时一直拿不到原生body:ReadableStream
一直报错 卡在这里



### 解决方案

fetch封装接口openAiDoor以及配置vite.config,ts

```ts
proxy.on('proxyReq', (proxyReq, req) => {
// 如果是 SSE 请求，告诉上游服务器不要缓冲
  if (req.headers.accept?.includes('text/event-stream')) {
    proxyReq.setHeader('Cache-Control', 'no-cache')
    proxyReq.setHeader('Connection', 'keep-alive')
  }
})
proxy.on('proxyRes', (proxyRes, req, res) => {
  // 确保 SSE 响应不被 Vite 中间层拦截或缓冲
  if (proxyRes.headers['content-type']?.includes('text/event-stream')) {
    // 关键：设置 X-Accel-Buffering 为 no，防止代理层缓冲
    res.setHeader('X-Accel-Buffering', 'no')
    res.setHeader('Cache-Control', 'no-cache')
    res.setHeader('Connection', 'keep-alive')
  }
})
```
### axios与fetch调用模型接口时的却别

#### Fetch 是浏览器原生 API，天生就是“流”的接口
它的核心设计是把响应体暴露为一个 ReadableStream（可读流）。可以通过 getReader() 一块一块地拿数据，不用等全部传输完。这在处理 AI 流式输出时是决定性的优势，因为能在第一个 token 到达时就立刻渲染出来。

### Axios是基于 XMLHttpRequest 的封装，是一个“批处理”接口
XHR 的设计理念是“等响应体全部接收完毕，再一次性交给你”。在浏览器端，你无法通过 XHR 拿到一个真正的流。所以 response.data 永远是在所有数据到齐后才被赋值的。即使它有 onDownloadProgress 回调，那也只是进度通知，你拿到的仍然是累积的全部数据，而不是“最新到达的那一小块”。


### SSE概念
SSE（Server-Sent Events，服务器推送事件）是 HTML5 规范里定义的一种服务器向浏览器单向推送数据的技术。

#### 执行方式
```text
浏览器 ──请求──> 服务器
浏览器 <──响应头（保持连接）── 服务器
浏览器 <──数据块 1── 服务器
浏览器 <──数据块 2── 服务器
浏览器 <──数据块 3── 服务器
...（连接一直开着，直到服务器主动关闭）
```
关键点：SSE 复用了 HTTP 协议，但把"响应"变成了一个持续打开的流。 


#### 问题1：可视化侧边菜单栏 跳转路由总是会回收
原因：顶层app.vue中使用 :key="route.path"
```vue
<router-view><component :is="Component" :key="route.path"/></router-view>
```
我子级菜单栏跳动  路由变化引起页面重新创建 导致侧边菜单栏被销毁 这个key值可以放在内部layout的<router-view>跳动口中

key的作用：路径一变，key 就变，强制销毁旧组件、创建新组件 保证数据干净