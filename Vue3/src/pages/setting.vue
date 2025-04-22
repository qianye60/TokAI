<template>
  <div class="profile">
    <div class="sidebar">
      <RouterLink to="/setting/modconfig" class="sidebar-item">
        <svg t="1744463640206" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2323" width="32" height="32"><path d="M968.9088 771.1744L512 1024l-3.4816-1.9456L51.2 769.024V254.976L512 0l460.8 254.976v514.048l-3.8912 2.1504zM392.192 401.2032l114.3808 56.1152 115.2-61.44L512 330.0352l-119.808 71.168zM543.4368 518.144v157.5936L664.576 603.648v-152.576L543.4368 518.144zM316.928 365.2608L512 247.9104l178.7904 105.984 154.624-85.9136L512 84.48 150.1184 284.3648l166.8096 80.896z m158.3104 307.6096V521.1136L359.424 464.384v139.3664l115.8144 69.12z m0 243.0976v-163.84L291.2256 643.3792V429.1584L122.1632 347.136v376.1152l353.0752 192.7168z m68.1984-158.3104v163.6352l358.4-200.704V317.3376l-169.0624 94.8224v231.2192L543.4368 757.6576z" fill="#231815" p-id="2324"></path></svg>
        <span class="item-span">模型参数</span>
      </RouterLink>
    </div>
    <div class="content-area">
      <RouterView/>
    </div>
  </div>
</template>

<script setup lang="ts">
import {RouterLink,RouterView,useRouter} from "vue-router"
const router = useRouter()
router.push("/setting/modconfig")
</script>

<style scoped>
.profile {
  height: 100%;
  width: 100%;
  position: relative;
  overflow: hidden;
}

.sidebar {
  position: absolute;
  left: 15px;
  top: 15px;
  bottom: 15px;
  width: 240px;
  background: linear-gradient(135deg, #1e88e5, #0d47a1);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 30px;
  overflow-y: auto;
  scrollbar-width: thin;
  box-shadow: 5px 0 20px rgba(0, 0, 0, 0.1);
  z-index: 2;
}

.sidebar::-webkit-scrollbar {
  width: 5px;
}

.sidebar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
}

.sidebar::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.sidebar-item{
  display: flex;
  justify-content: flex-start;
  align-items: center;
  width: 85%;
  height: 50px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  margin: 10px 0;
  padding: 0 15px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  overflow: hidden;
  text-decoration: none;
  backdrop-filter: blur(5px);
}

.sidebar-item:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-3px);
  box-shadow: 0 7px 14px rgba(0, 0, 0, 0.2);
}

.sidebar-item::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: #ffffff;
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.sidebar-item:hover::before,
.sidebar-item.router-link-active::before {
  transform: scaleY(1);
}

.sidebar-item.router-link-active {
  background-color: rgba(255, 255, 255, 0.25);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.item-span {
  color: white;
  font-weight: 500;
  margin-left: 12px;
  font-size: 15px;
  letter-spacing: 0.5px;
}

.icon {
  filter: brightness(0) invert(1);
  opacity: 0.9;
  transition: opacity 0.3s ease;
}

.sidebar-item:hover .icon {
  opacity: 1;
}

/* 右侧内容区域 */
.content-area {
  position: absolute;
  left: 270px;
  right: 15px;
  top: 15px;
  bottom: 15px;
  padding: 30px;
  overflow-y: auto;
  background-color: var(--background-color);
  border-radius: 20px 0 0 20px;
  box-shadow: -5px 0 20px rgba(0, 0, 0, 0.05);
}

/* 手机端样式适配 */
@media screen and (max-width: 768px) {
  .profile {
    position: static;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .sidebar {
    position: absolute;
    left: auto;
    top: auto;
    bottom: auto;
    width: 92%;
    height: auto;
    max-height: 80px;
    flex-direction: row;
    justify-content: flex-start;
    padding: 10px;
    margin: 10px auto;
    overflow-x: auto;
    overflow-y: hidden;
  }
  
  .sidebar::-webkit-scrollbar {
    display: none;
  }
  
  .sidebar-item {
    width: auto;
    min-width: 140px;
    height: 50px;
    margin: 0 8px;
    flex-shrink: 0;
  }
  
  .sidebar-item::before {
    width: 100%;
    height: 4px;
    top: 0;
    left: 0;
    transform: scaleX(0);
  }
  
  .sidebar-item:hover::before,
  .sidebar-item.router-link-active::before {
    transform: scaleX(1);
  }
  
  .content-area {
    position: relative;
    left: auto;
    right: auto;
    top: auto;
    bottom: auto;
    width: 100%;
    margin: 0;
    border-radius: 20px;
    padding: 0px;
    margin-top: 5rem;
  }
}
</style>