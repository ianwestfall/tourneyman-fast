<template>
  <div class="global-alerts container">
    <alert
      v-for="(alert, index) in alerts"
      :key="index"
      :alert="alert"
    />
  </div>
</template>

<script>
import Alert from '@/components/alerts/Alert.vue';

export default {
  name: 'Alerts',
  components: { Alert },
  computed: {
    alerts() {
      return this.$store.getters['alerts/getAlerts'];
    },
  },
};
</script>

<style lang="less" scoped>
.global-alerts {
  position: fixed;
  z-index: 999;
  top: 65px;
  margin: 0 25%;
  width: 50%;
  left: 0;
}
</style>
