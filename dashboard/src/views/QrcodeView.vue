<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiCamera" title="QR Code" main>
      </SectionTitleLineWithButton>
      <div class="col-lg-12 grid-margin stretch-card">
        <div class="card">
          <div class="card-body">
            <!-- <h4 class="card-title">Webcam</h4> -->
            <div class="video-container">
              <video ref="videoElement" autoplay></video>
            </div>
          </div>
        </div>
      </div>
      <BaseDivider />
    </SectionMain>
  </LayoutAuthenticated>
</template>

<script lang="ts">
export default {
  mounted() {
    this.startWebcam();
  },
  beforeUnmount() {
    this.stopWebcam();
  },
  methods: {
    startWebcam() {
      if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
          .then((stream) => {
            this.$refs.videoElement.srcObject = stream;
          })
          .catch((error) => {
            console.error('Error accessing the webcam', error);
          });
      }
    },
    stopWebcam() {
      const stream = this.$refs.videoElement.srcObject;
      const tracks = stream.getTracks();

      tracks.forEach(track => {
        track.stop();
      });

      this.$refs.videoElement.srcObject = null;
    }
  }
};
</script>

<script setup lang="ts">
import LayoutAuthenticated        from '@/layouts/LayoutAuthenticated.vue';
import SectionMain                from '@/components/SectionMain.vue'
import BaseDivider                from '@/components/BaseDivider.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import { mdiCamera }              from '@mdi/js'
</script>

<style scoped lang="scss">
.chartjs {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.video-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80vw;
  max-width: 600px;
  aspect-ratio: 1;
  overflow: hidden;
  margin: 0 auto;
}

video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (max-width: 768px) {
  .video-container {
    width: 90vw;
    max-width: none;
  }
}

@media (max-width: 480px) {
  .video-container {
    width: 100vw;
    aspect-ratio: auto;
  }
}
</style>
