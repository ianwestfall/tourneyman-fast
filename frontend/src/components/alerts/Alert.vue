<template>
  <b-alert
    class="global-alert"
    :show="dismissCountDown"
    dismissible
    :variant="alert.type"
    @dismissed="dismissCountDown = 0"
    @dismiss-count-down="countDownChanged"
  >{{ alert.message }}</b-alert>
</template>

<script>
export default {
  name: 'Alert',
  props: {
    alert: Object,
  },
  mounted() {
    this.showAlert();
  },
  data() {
    return {
      dismissSecs: 10,
      dismissCountDown: 0,
      showDismissibleAlert: true,
    };
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    showAlert() {
      this.dismissCountDown = this.dismissSecs;
    },
  },
};
</script>

<style lang="less" scoped>
.global-alert {
  text-align: center;
  opacity: 0.75;
}
</style>
