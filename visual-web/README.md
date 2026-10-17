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

## Vue 3 + TypeScript 响应式数据与第三方复杂类型

### 问题示例：把 ECharts 配置放进 `ref`

图表组件接收的配置属性声明为 ECharts 自己的类型：

```ts
// 子组件
const props = defineProps<{
  baseOption: EChartsOption
}>()
```

在 `src/views/v-scorll/view-scroll.vue` 中，`barBaseOption` 本身已经在 `ref` 外面声明；但如果像下面这样再把它和普通业务数据一起放进深层响应式的 `ref`，并从模板传给 `vPictorialBar`：

```ts
interface chartItem {
  baseOption: EChartsOption
  optionData: SomeData[]
}

const aiDistrition = ref<chartItem>({
  baseOption: barBaseOption,
  optionData: [],
})
```

```vue
<vPictorialBar :base-option="aiDistrition.baseOption" />
```

就可能在 `view-scroll.vue` 的 `:base-option="aiDistrition.baseOption"` 处遇到类似下面的类型错误：

```text
Type ... is not assignable to type 'EChartsOption'
```

错误信息有时会展开成非常长的类型链，例如从 `graphic`、`keyframeAnimation` 一路指向 `textContent`。这不一定表示配置对象里实际写了这些字段；`EChartsOption` 本身是一个包含许多可选配置和复杂联合类型的完整类型，TypeScript 检查的是整个类型是否兼容。

### 为什么会这样

1. `ref<T>()` 不只是给值加上 `.value`。Vue 的 `ref` 会把对象转换成深层响应式对象，其公开类型可以近似理解为 `Ref<UnwrapRef<T>>`。
2. 这个转换会递归处理对象的属性。普通业务对象通常适合深层响应式，但 ECharts 配置是第三方库定义的复杂类型；类型中包含联合类型、回调、图形元素以及和渲染器相关的对象。
3. 递归转换后的类型不一定还能与原始 `EChartsOption` 完全兼容。即使运行时的配置内容有效，TypeScript 也可能因为转换后某个很深的成员类型发生变化而拒绝把它传给子组件。
4. Vue 模板会自动解包 `ref`，因此模板中的 `chartItem.baseOption` 实际上是访问响应式值里的 `baseOption`。这个自动解包不会把其内部复杂类型恢复成原始的 `EChartsOption`。

因此，本例的根因是“把第三方复杂配置放入深层 `ref` 后发生的类型不兼容”，而不是 kebab-case 属性名。Vue 会将模板中的 `base-option` 对应到子组件声明的 `baseOption`；这种命名转换是正常用法。

### 推荐做法：把静态配置和响应式业务数据分开

如果配置只在初始化时定义、不会作为响应式状态整体替换，就不要把配置放进 `ref`。只让确实会变化的数据保持响应式：

```ts
const barBaseOption: EChartsOption = {
  // ECharts 配置
}

const aiDistrition = ref<{ optionData: SomeData[] }>({
  optionData: [],
})
```

```vue
<vPictorialBar
  :base-option="barBaseOption"
  :option-data="aiDistrition.optionData"
/>
```

模板会自动解包 `optionData`，而 `barBaseOption` 保持原始 `EChartsOption` 类型。这通常也是图表配置最简单、最清晰的组织方式。`SomeData` 应替换为项目中接口返回数据的真实类型，避免用 `any` 放弃检查。

### 需要把配置放在响应式容器中时

如果配置需要作为一个整体被替换，可以使用 `shallowRef`，避免 Vue 对配置对象做递归响应式转换：

```ts
const chartItem = shallowRef<ChartItem>({
  baseOption: barBaseOption,
  optionData: [],
})
```

`shallowRef` 只追踪 `.value` 的替换，不会自动追踪对象内部属性的原地修改。因此，更新内部数据时应创建新对象并替换 `.value`：

```ts
chartItem.value = {
  ...chartItem.value,
  optionData: nextData,
}
```

若唯一需要响应式更新的是数据数组，优先采用上一节的“配置常量 + 独立数据 `ref`”，不要为了让类型通过而盲目把整个对象换成 `shallowRef`。

### 后续编写组件属性的准则

1. **先确认属性两端的类型一致。** 子组件用 `defineProps` 声明的类型应与父组件传入值的真实类型一致；模板可用 kebab-case，脚本类型仍用 camelCase。
2. **区分配置与状态。** 图表配置、编辑器配置等大型第三方配置对象，若不需要深层响应式，不要放进普通 `ref` 或 `reactive`。把会变化的业务数据独立管理。
3. **选对响应式容器。** 普通表单/业务对象使用 `ref` 或 `reactive`；复杂第三方对象优先保持普通常量，确需替换时考虑 `shallowRef`，并按整体替换的方式更新。
4. **不要用类型断言掩盖问题。** 不要用 `as any`、把子组件属性改成 `any` 或随意强转来消除红线；这会隐藏真正的父子类型不匹配，也会让后续错误更难定位。
5. **沿类型错误链找第一个不兼容点。** 检查父组件值的声明、是否经过 `ref`/`reactive` 深层转换，以及子组件属性声明。长错误链最深处往往只是 TypeScript 找到的差异位置，不一定是要修改的实际业务字段。
6. **用项目类型检查验证。** 在 `visual-web` 目录运行 `npm run type-check`。如果输出中还有其他文件的错误，应分别处理；单个属性修正并不保证整个项目类型检查全部通过。


#### 问题1：可视化侧边菜单栏 跳转路由总是会回收
原因：顶层app.vue中使用 :key="route.path"
```vue
<router-view><component :is="Component" :key="route.path"/></router-view>
```
我子级菜单栏跳动  路由变化引起页面重新创建 导致侧边菜单栏被销毁 这个key值可以放在内部layout的<router-view>跳动口中

key的作用：路径一变，key 就变，强制销毁旧组件、创建新组件 保证数据干净

【要做什么】
开发一个左边图表类型选择域  中间预览  右边配置  页面 用echarts开发 图表配置出来需要开发  配置可以选数据 主题 颜色 元素颜色 

【背景 / 现状】
菜单表你已知 数据库已有 文件你可以读取

【预期结果】
功能完善，注释清晰，无明显错误

【范围】
涉及哪些页面、接口或文件？哪些内容不要改？

【技术或业务约束】
例如：必须使用现有组件、接口格式、数据库字段、兼容某些浏览器。

【验证方式】
希望运行哪些测试、命令，或怎样确认功能完成？

【其他要求】
注释、类型、文档、界面风格、Git 操作等特别要求。