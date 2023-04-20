<template>
    <div class="profile-form" v-if="items.length">
        <div class="profile-user-info profile-user-info-striped">
            <div class="profile-info-row" v-for="item in items"> 
                <div class="profile-info-name">{{item.name}}</div>
                <div class="profile-info-value ">{{item.value|nullEmpty}}</div>
            </div>
        </div>
    </div>
</template>

<script>
import './profile-form.less'
export default {
    name: "ProfileForm",
    props: [
      'items',//profile form item list
    ],
    data() {
      return {
      }
    },
    filters: {
        nullEmpty: function (value) {
           if (!value || value === '') value = '-';
           return value;
        }
    }
}
</script>

<style scoped>
</style>