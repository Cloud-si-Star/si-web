<template>
  <div class="chat-avatar" :class="`chat-avatar--${type}`" :style="{ width: size + 'px', height: size + 'px' }">
    <!-- ============ 用户头像：小猫 ============ -->
    <svg v-if="type === 'user'" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" class="chat-avatar__svg">
      <defs>
        <linearGradient id="catBodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#667eea" stop-opacity="0.9" />
          <stop offset="50%" stop-color="#764ba2" stop-opacity="0.75" />
          <stop offset="100%" stop-color="#4facfe" stop-opacity="0.85" />
        </linearGradient>
        <linearGradient id="earGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#a18cd1" stop-opacity="0.9" />
          <stop offset="100%" stop-color="#667eea" stop-opacity="0.8" />
        </linearGradient>
        <radialGradient id="eyeGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="1" />
          <stop offset="30%" stop-color="#00e5ff" stop-opacity="0.9" />
          <stop offset="100%" stop-color="#00e5ff" stop-opacity="0" />
        </radialGradient>
        <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.6" />
          <stop offset="50%" stop-color="#b388ff" stop-opacity="0.3" />
          <stop offset="100%" stop-color="#00e5ff" stop-opacity="0.6" />
        </linearGradient>
        <linearGradient id="circuitGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#00e5ff" stop-opacity="0" />
          <stop offset="50%" stop-color="#00e5ff" stop-opacity="0.7" />
          <stop offset="100%" stop-color="#00e5ff" stop-opacity="0" />
        </linearGradient>
        <filter id="catBlur6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" /></filter>
        <filter id="catBlur3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" /></filter>
        <filter id="catBlur10" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10" /></filter>
      </defs>

      <circle cx="100" cy="100" r="85" fill="#667eea" opacity="0.08" filter="url(#catBlur10)" />
      <circle cx="100" cy="100" r="70" fill="#00e5ff" opacity="0.06" filter="url(#catBlur6)" />

      <circle cx="100" cy="100" r="82" fill="none" stroke="url(#ringGrad)" stroke-width="1.5" opacity="0.5" />
      <circle cx="100" cy="100" r="88" fill="none" stroke="#00e5ff" stroke-width="0.8" opacity="0.2" stroke-dasharray="4 8" />

      <circle cx="100" cy="12" r="2" fill="#00e5ff" opacity="0.8" />
      <circle cx="188" cy="100" r="2" fill="#b388ff" opacity="0.6" />
      <circle cx="100" cy="188" r="2" fill="#00e5ff" opacity="0.6" />
      <circle cx="12" cy="100" r="2" fill="#b388ff" opacity="0.8" />

      <path d="M 100 25 L 100 35" stroke="url(#circuitGrad)" stroke-width="1" fill="none" />
      <path d="M 175 100 L 165 100" stroke="url(#circuitGrad)" stroke-width="1" fill="none" />
      <path d="M 100 175 L 100 165" stroke="url(#circuitGrad)" stroke-width="1" fill="none" />
      <path d="M 25 100 L 35 100" stroke="url(#circuitGrad)" stroke-width="1" fill="none" />

      <path d="M 55 75 L 45 40 L 80 60 Z" fill="url(#earGrad)" opacity="0.85" />
      <path d="M 145 75 L 155 40 L 120 60 Z" fill="url(#earGrad)" opacity="0.85" />
      <path d="M 57 68 L 52 48 L 72 60 Z" fill="#ff9ff3" opacity="0.4" />
      <path d="M 143 68 L 148 48 L 128 60 Z" fill="#ff9ff3" opacity="0.4" />

      <ellipse cx="100" cy="105" rx="50" ry="45" fill="url(#catBodyGrad)" opacity="0.7" />
      <ellipse cx="85" cy="90" rx="20" ry="15" fill="#ffffff" opacity="0.15" filter="url(#catBlur6)" />
      <ellipse cx="115" cy="88" rx="12" ry="8" fill="#ffffff" opacity="0.1" filter="url(#catBlur3)" />

      <circle cx="80" cy="100" r="14" fill="url(#eyeGlow)" opacity="0.6" filter="url(#catBlur6)" />
      <circle cx="120" cy="100" r="14" fill="url(#eyeGlow)" opacity="0.6" filter="url(#catBlur6)" />

      <ellipse cx="80" cy="100" rx="8" ry="9" fill="#1a1a2e" opacity="0.9" />
      <ellipse cx="120" cy="100" rx="8" ry="9" fill="#1a1a2e" opacity="0.9" />

      <circle cx="77" cy="97" r="2.5" fill="#ffffff" opacity="0.95" />
      <circle cx="117" cy="97" r="2.5" fill="#ffffff" opacity="0.95" />
      <circle cx="82" cy="103" r="1.2" fill="#00e5ff" opacity="0.8" />
      <circle cx="122" cy="103" r="1.2" fill="#00e5ff" opacity="0.8" />

      <path d="M 96 118 L 104 118 L 100 123 Z" fill="#ff6b9d" opacity="0.9" />

      <path d="M 100 123 Q 95 128 90 126" stroke="#333" stroke-width="1.2" fill="none" opacity="0.6" stroke-linecap="round" />
      <path d="M 100 123 Q 105 128 110 126" stroke="#333" stroke-width="1.2" fill="none" opacity="0.6" stroke-linecap="round" />

      <line x1="55" y1="115" x2="35" y2="110" stroke="#666" stroke-width="0.8" opacity="0.4" stroke-linecap="round" />
      <line x1="55" y1="120" x2="35" y2="120" stroke="#666" stroke-width="0.8" opacity="0.4" stroke-linecap="round" />
      <line x1="55" y1="125" x2="35" y2="130" stroke="#666" stroke-width="0.8" opacity="0.4" stroke-linecap="round" />
      <line x1="145" y1="115" x2="165" y2="110" stroke="#666" stroke-width="0.8" opacity="0.4" stroke-linecap="round" />
      <line x1="145" y1="120" x2="165" y2="120" stroke="#666" stroke-width="0.8" opacity="0.4" stroke-linecap="round" />
      <line x1="145" y1="125" x2="165" y2="130" stroke="#666" stroke-width="0.8" opacity="0.4" stroke-linecap="round" />

      <ellipse cx="68" cy="115" rx="6" ry="4" fill="#ff9ff3" opacity="0.3" filter="url(#catBlur3)" />
      <ellipse cx="132" cy="115" rx="6" ry="4" fill="#ff9ff3" opacity="0.3" filter="url(#catBlur3)" />

      <circle cx="60" cy="55" r="1.5" fill="#00e5ff" opacity="0.7" />
      <circle cx="140" cy="55" r="1.5" fill="#b388ff" opacity="0.7" />
      <circle cx="50" cy="135" r="1.5" fill="#00e5ff" opacity="0.5" />
      <circle cx="150" cy="135" r="1.5" fill="#b388ff" opacity="0.5" />
      <circle cx="100" cy="35" r="1" fill="#ffffff" opacity="0.6" />
      <circle cx="100" cy="165" r="1" fill="#ffffff" opacity="0.6" />
    </svg>

    <!-- ============ AI 头像：球形机器人核心 ============ -->
    <svg v-else viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" class="chat-avatar__svg">
      <defs>
        <!-- 玻璃球体渐变 -->
        <radialGradient id="sphereGrad" cx="35%" cy="30%" r="80%">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9" />
          <stop offset="40%" stop-color="#b8e0ff" stop-opacity="0.5" />
          <stop offset="100%" stop-color="#4a90d9" stop-opacity="0.3" />
        </radialGradient>
        <!-- 脸部屏幕渐变 -->
        <radialGradient id="screenGrad" cx="50%" cy="40%" r="70%">
          <stop offset="0%" stop-color="#0d2a4a" />
          <stop offset="100%" stop-color="#05101f" />
        </radialGradient>
        <!-- 屏幕边框发光 -->
        <linearGradient id="screenBorder" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#00e5ff" />
          <stop offset="50%" stop-color="#00b7ff" />
          <stop offset="100%" stop-color="#00e5ff" />
        </linearGradient>
        <!-- 能量波渐变 -->
        <linearGradient id="energyGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#00e5ff" stop-opacity="0" />
          <stop offset="50%" stop-color="#64ffda" stop-opacity="0.6" />
          <stop offset="100%" stop-color="#00e5ff" stop-opacity="0" />
        </linearGradient>
        <!-- 点阵图案 -->
        <pattern id="dotMatrix" x="0" y="0" width="4" height="4" patternUnits="userSpaceOnUse">
          <circle cx="2" cy="2" r="1" fill="#ffffff" />
        </pattern>
        <pattern id="dotMatrixGlow" x="0" y="0" width="4" height="4" patternUnits="userSpaceOnUse">
          <circle cx="2" cy="2" r="1.2" fill="#00e5ff" />
        </pattern>
        <!-- 眼睛发光 -->
        <radialGradient id="aiEyeGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#ffffff" />
          <stop offset="60%" stop-color="#80f0ff" />
          <stop offset="100%" stop-color="#00e5ff" stop-opacity="0" />
        </radialGradient>
        <filter id="aiBlur4" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" /></filter>
        <filter id="aiBlur8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8" /></filter>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="3" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      <!-- 背景光晕 -->
      <circle cx="100" cy="100" r="90" fill="#4fc3f7" opacity="0.1" filter="url(#aiBlur8)" />

      <!-- 玻璃球体外壳 -->
      <circle cx="100" cy="100" r="78" fill="url(#sphereGrad)" stroke="#ffffff" stroke-width="1.5" opacity="0.85" />

      <!-- 球体高光 -->
      <ellipse cx="75" cy="70" rx="28" ry="18" fill="#ffffff" opacity="0.35" filter="url(#aiBlur4)" />

      <!-- 机械接缝线 -->
      <path d="M 100 22 L 100 55" stroke="#7ab8e0" stroke-width="1" opacity="0.5" />
      <path d="M 100 145 L 100 178" stroke="#7ab8e0" stroke-width="1" opacity="0.5" />
      <path d="M 22 100 L 50 100" stroke="#7ab8e0" stroke-width="1" opacity="0.5" />
      <path d="M 150 100 L 178 100" stroke="#7ab8e0" stroke-width="1" opacity="0.5" />

      <!-- 能量波装饰 -->
      <path d="M 35 80 Q 50 75 60 80" stroke="url(#energyGrad)" stroke-width="1.5" fill="none" opacity="0.6" />
      <path d="M 140 80 Q 150 75 165 80" stroke="url(#energyGrad)" stroke-width="1.5" fill="none" opacity="0.6" />
      <path d="M 35 120 Q 50 125 60 120" stroke="url(#energyGrad)" stroke-width="1.5" fill="none" opacity="0.4" />
      <path d="M 140 120 Q 150 125 165 120" stroke="url(#energyGrad)" stroke-width="1.5" fill="none" opacity="0.4" />

      <!-- 侧耳 -->
      <ellipse cx="24" cy="100" rx="6" ry="12" fill="#c8e6ff" stroke="#7ab8e0" stroke-width="1" opacity="0.8" />
      <ellipse cx="176" cy="100" rx="6" ry="12" fill="#c8e6ff" stroke="#7ab8e0" stroke-width="1" opacity="0.8" />
      <ellipse cx="24" cy="100" rx="2.5" ry="6" fill="#00e5ff" opacity="0.6" />
      <ellipse cx="176" cy="100" rx="2.5" ry="6" fill="#00e5ff" opacity="0.6" />

      <!-- 脸部屏幕背景发光 -->
      <rect x="48" y="62" width="104" height="76" rx="20" fill="#00e5ff" opacity="0.2" filter="url(#aiBlur8)" />

      <!-- 脸部屏幕 -->
      <rect x="50" y="64" width="100" height="72" rx="18" fill="url(#screenGrad)" stroke="url(#screenBorder)" stroke-width="2" filter="url(#glow)" />

      <!-- 点阵屏纹理 -->
      <rect x="50" y="64" width="100" height="72" rx="18" fill="url(#dotMatrix)" opacity="0.06" />

      <!-- 眼睛发光层 -->
      <circle cx="80" cy="95" r="13" fill="url(#aiEyeGlow)" opacity="0.5" filter="url(#aiBlur4)" />
      <circle cx="120" cy="95" r="13" fill="url(#aiEyeGlow)" opacity="0.5" filter="url(#aiBlur4)" />

      <!-- 点阵眼睛 -->
      <circle cx="80" cy="95" r="9" fill="url(#dotMatrixGlow)" filter="url(#glow)" />
      <circle cx="120" cy="95" r="9" fill="url(#dotMatrixGlow)" filter="url(#glow)" />

      <!-- 眼睛中心亮点 -->
      <circle cx="80" cy="95" r="3.5" fill="#ffffff" />
      <circle cx="120" cy="95" r="3.5" fill="#ffffff" />

      <!-- 点阵微笑 -->
      <path d="M 88 116 Q 100 123 112 116" stroke="#00e5ff" stroke-width="3" fill="none" stroke-linecap="round" filter="url(#glow)" />
      <circle cx="92" cy="119" r="1.5" fill="#00e5ff" />
      <circle cx="100" cy="121" r="1.5" fill="#00e5ff" />
      <circle cx="108" cy="119" r="1.5" fill="#00e5ff" />

      <!-- 底部装饰点 -->
      <circle cx="100" cy="172" r="2" fill="#00e5ff" opacity="0.7" />
      <circle cx="85" cy="172" r="1.2" fill="#64ffda" opacity="0.5" />
      <circle cx="115" cy="172" r="1.2" fill="#64ffda" opacity="0.5" />
    </svg>
  </div>
</template>

<script setup lang="ts">
interface Props {
  /** 头像类型：user=小猫用户头像，ai=机器人AI头像 */
  type?: 'user' | 'ai'
  /** 头像尺寸（px），默认 36 */
  size?: number
}

withDefaults(defineProps<Props>(), {
  type: 'user',
  size: 36,
})
</script>

<style lang="scss" scoped>
.chat-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  transition: transform 0.25s ease;

  &__svg {
    width: 100%;
    height: 100%;
  }

  &--user:hover {
    transform: scale(1.20);
    cursor: pointer;
  }

  &--ai:hover {
    transform: scale(1.20);
    cursor: pointer;
  }
}
</style>
