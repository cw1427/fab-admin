<template>
<Affix>
<div id="fh5co-page">
    <header id="fh5co-header" role="banner">
        <div class="container">
            <div class="row">
                <div class="header-inner">
                    <h1><a :href="baseURL">{* app_name *}<span></span></a></h1>
                    <nav role="navigation">
                        <ul>
                            <li><a href="#autodoc">API Document</a></li>
                            <li><a href="#feature">Feature</a></li>
                            <li class="cta"><a href="/switch/original">Old UI</a></li>
                        </ul>
                    </nav>
                </div>
            </div>
        </div>
    </header>
</div>
</Affix>
</template>

<script>
import { Affix } from 'iview'
import baseURL from '_conf/url'
export default {
  name: 'IndexHeader',
  data () {
    return {
        baseURL,
    }
  },
  props: {

  },
  methods: {

  }
}
</script>

<style>
</style>

