<template>
  <div>
    <Button size="large" type="text" @click="backHome">Back to Home</Button>
    <Button size="large" type="text">Back to last page({{ second }}s)</Button>
  </div>
</template>

<script>
import './error.less'
export default {
  name: 'backBtnGroup',
  data () {
    return {
      second: 5,
      timer: null
    }
  },
  methods: {
    backHome () {
      this.$router.replace({
        name: 'main'
      })
    },
    backPrev () {
      this.$router.go(-1)
    }
  },
  mounted () {
    this.timer = setInterval(() => {
      if (this.second === 0) this.backPrev()
      else this.second--
    }, 1000)
  },
  beforeDestroy () {
    clearInterval(this.timer)
  }
}
</script>
