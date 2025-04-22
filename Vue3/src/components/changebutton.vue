<script setup lang="ts">
import {ref, watch, onMounted, onBeforeMount} from 'vue'
import {useSystemConfig} from '@/store/dataconfig.ts'
const SystemConfig = useSystemConfig()

// 监听主题变化
watch(() => SystemConfig.theme, (newVal) => {
  document.documentElement.setAttribute('data-theme', newVal ? 'dark' : 'light')
})

// 初始化时设置主题
onMounted(() => {
  document.documentElement.setAttribute('data-theme', SystemConfig.theme ? 'dark' : 'light')
})
</script>

<template>
  <label class="switch">
    <input id="input" type="checkbox" v-model="SystemConfig.theme"/>
    <div class="slider round">
      <div class="sun-moon">
        <svg id="moon-dot-1" class="moon-dot" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>
        <svg id="moon-dot-2" class="moon-dot" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>
        <svg id="moon-dot-3" class="moon-dot" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>
        <svg id="light-ray-1" class="light-ray" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>
        <svg id="light-ray-2" class="light-ray" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>
        <svg id="light-ray-3" class="light-ray" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>

        <svg id="cloud-1" class="cloud-dark" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>
        <svg id="cloud-2" class="cloud-dark" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>
        <svg id="cloud-3" class="cloud-dark" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>
        <svg id="cloud-4" class="cloud-light" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>
        <svg id="cloud-5" class="cloud-light" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>
        <svg id="cloud-6" class="cloud-light" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="50"></circle>
        </svg>
      </div>
      <div class="stars">
        <svg id="star-1" class="star" viewBox="0 0 20 20">
          <path
            d="M 0 10 C 10 10,10 10 ,0 10 C 10 10 , 10 10 , 10 20 C 10 10 , 10 10 , 20 10 C 10 10 , 10 10 , 10 0 C 10 10,10 10 ,0 10 Z"
          ></path>
        </svg>
        <svg id="star-2" class="star" viewBox="0 0 20 20">
          <path
            d="M 0 10 C 10 10,10 10 ,0 10 C 10 10 , 10 10 , 10 20 C 10 10 , 10 10 , 20 10 C 10 10 , 10 10 , 10 0 C 10 10,10 10 ,0 10 Z"
          ></path>
        </svg>
        <svg id="star-3" class="star" viewBox="0 0 20 20">
          <path
            d="M 0 10 C 10 10,10 10 ,0 10 C 10 10 , 10 10 , 10 20 C 10 10 , 10 10 , 20 10 C 10 10 , 10 10 , 10 0 C 10 10,10 10 ,0 10 Z"
          ></path>
        </svg>
        <svg id="star-4" class="star" viewBox="0 0 20 20">
          <path
            d="M 0 10 C 10 10,10 10 ,0 10 C 10 10 , 10 10 , 10 20 C 10 10 , 10 10 , 20 10 C 10 10 , 10 10 , 10 0 C 10 10,10 10 ,0 10 Z"
          ></path>
        </svg>
      </div>
    </div>
  </label>
</template>

<style scoped>
  .switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
  }

  .switch #input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #2196f3;
    -webkit-transition: 0.4s;
    transition: 0.4s;
    z-index: 0;
    overflow: hidden;
  }

  .sun-moon {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: yellow;
    -webkit-transition: 0.4s;
    transition: 0.4s;
  }

  #input:checked + .slider {
    background-color: black;
  }

  #input:focus + .slider {
    box-shadow: 0 0 1px #2196f3;
  }

  #input:checked + .slider .sun-moon {
    -webkit-transform: translateX(26px);
    -ms-transform: translateX(26px);
    transform: translateX(26px);
    background-color: white;
    -webkit-animation: rotate-center 0.6s ease-in-out both;
    animation: rotate-center 0.6s ease-in-out both;
  }

  .moon-dot {
    opacity: 0;
    transition: 0.4s;
    fill: gray;
  }

  #input:checked + .slider .sun-moon .moon-dot {
    opacity: 1;
  }

  .slider.round {
    border-radius: 34px;
  }

  .slider.round .sun-moon {
    border-radius: 50%;
  }

  #moon-dot-1 {
    left: 10px;
    top: 3px;
    position: absolute;
    width: 6px;
    height: 6px;
    z-index: 4;
  }

  #moon-dot-2 {
    left: 2px;
    top: 10px;
    position: absolute;
    width: 10px;
    height: 10px;
    z-index: 4;
  }

  #moon-dot-3 {
    left: 16px;
    top: 18px;
    position: absolute;
    width: 3px;
    height: 3px;
    z-index: 4;
  }

  #light-ray-1 {
    left: -8px;
    top: -8px;
    position: absolute;
    width: 43px;
    height: 43px;
    z-index: -1;
    fill: white;
    opacity: 10%;
  }

  #light-ray-2 {
    left: -50%;
    top: -50%;
    position: absolute;
    width: 55px;
    height: 55px;
    z-index: -1;
    fill: white;
    opacity: 10%;
  }

  #light-ray-3 {
    left: -18px;
    top: -18px;
    position: absolute;
    width: 60px;
    height: 60px;
    z-index: -1;
    fill: white;
    opacity: 10%;
  }

  .cloud-light {
    position: absolute;
    fill: #eee;
    animation-name: cloud-move;
    animation-duration: 6s;
    animation-iteration-count: infinite;
  }

  .cloud-dark {
    position: absolute;
    fill: #ccc;
    animation-name: cloud-move;
    animation-duration: 6s;
    animation-iteration-count: infinite;
    animation-delay: 1s;
  }

  #cloud-1 {
    left: 30px;
    top: 15px;
    width: 40px;
  }

  #cloud-2 {
    left: 44px;
    top: 10px;
    width: 20px;
  }

  #cloud-3 {
    left: 18px;
    top: 24px;
    width: 30px;
  }

  #cloud-4 {
    left: 36px;
    top: 18px;
    width: 40px;
  }

  #cloud-5 {
    left: 48px;
    top: 14px;
    width: 20px;
  }

  #cloud-6 {
    left: 22px;
    top: 26px;
    width: 30px;
  }

  @keyframes cloud-move {
    0% {
      transform: translateX(0px);
    }

    40% {
      transform: translateX(4px);
    }

    80% {
      transform: translateX(-4px);
    }

    100% {
      transform: translateX(0px);
    }
  }

  .stars {
    transform: translateY(-32px);
    opacity: 0;
    transition: 0.4s;
  }

  .star {
    fill: white;
    position: absolute;
    -webkit-transition: 0.4s;
    transition: 0.4s;
    animation-name: star-twinkle;
    animation-duration: 2s;
    animation-iteration-count: infinite;
  }

  #input:checked + .slider .stars {
    -webkit-transform: translateY(0);
    -ms-transform: translateY(0);
    transform: translateY(0);
    opacity: 1;
  }

  #star-1 {
    width: 20px;
    top: 2px;
    left: 3px;
    animation-delay: 0.3s;
  }

  #star-2 {
    width: 6px;
    top: 16px;
    left: 3px;
  }

  #star-3 {
    width: 12px;
    top: 20px;
    left: 10px;
    animation-delay: 0.6s;
  }

  #star-4 {
    width: 18px;
    top: 0px;
    left: 18px;
    animation-delay: 1.3s;
  }

  @keyframes star-twinkle {
    0% {
      transform: scale(1);
    }

    40% {
      transform: scale(1.2);
    }

    80% {
      transform: scale(0.8);
    }

    100% {
      transform: scale(1);
    }
  }
</style>
