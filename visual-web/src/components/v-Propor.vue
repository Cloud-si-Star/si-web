<template>
    <div class="svg-border">
        <svg viewBox="0 0 200 100" preserveAspectRatio="none">
            <rect x="1" y="1" width="198" height="98" rx="10"
                fill="none" stroke="#00e5ff" stroke-width="2"
                stroke-dasharray="40 260" class="svg-border__line" />
        </svg>
        <div class="svg-border__content">内容</div>
    </div>
</template>

<script setup lang="ts">


</script>

<style lang="scss" scoped>
.svg-border {
  height: 100%;
  width: 100%;
}

.svg-border svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.svg-border__line {
  animation: dash 3s linear infinite;
  filter: drop-shadow(0 0 4px #00e5ff); /* 轻微发光，可去掉 */
}

@keyframes dash {
  to { stroke-dashoffset: -300; }
}
</style>