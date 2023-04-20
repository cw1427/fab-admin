<template>
	<Carousel loop arrow="never" dots="outside" v-model="slideIndex" style="padding-bottom:0%;height:600px;width: 100%">
            <CarouselItem>
                <ApidocCard></ApidocCard>
            </CarouselItem>
    </Carousel>
</template>

<script>
import { Message,Spin,LoadingBar } from 'iview'
import ApidocCard from '@/view/components/apidoc-card'
export default {
  name: 'IndexSlider',
  components: {
      ApidocCard
  },
  data () {
    return {
        
    }
  },
  created() {
  },
  props: [
      "slideIndex"
  ],
  methods: {
  },
  filters: {
  }
}
</script>

<style scoped>
</style>
