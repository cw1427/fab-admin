<template>
    <Card style="height:300px">
        <p slot="title" style="height:120px">
            <Row type="flex" align="middle" :gutter="10">
                <Col span="8"><img :src="avator_big" class="user-card-avator-img"></img></Col>
                <Col span="16">
                    <Row>
                        <Col><b class="user-card-infor-name">{{userName}}</b></Col>
                        <Col>
                             <p>{{loginName}}</p>
                        </Col>
                    </Row>
                </Col>
            </Row>
        </p>
        <a href="#" slot="extra" @click.prevent="gotoProfile">
            <Icon type="person"></Icon>
            Profile
        </a>

        <div class="profile-user-info profile-user-info-striped">
            <div class="profile-info-row ">
                <div class="profile-info-name">User id</div>
                <div class="profile-info-value ">{{userId}}</div>
            </div>
             <div class="profile-info-row ">
                <div class="profile-info-name">Roles</div>
                <div class="profile-info-value ">
                    <template v-for="role in accesses">
                       {{role}}&nbsp;&nbsp;
                    </template>
                </div>
            </div>
            <div class="profile-info-row ">
                <div class="profile-info-name">Last login</div>
                <div class="profile-info-value ">{{lastLogin}}</div>
            </div>
        </div>
    </Card>
</template>

<script>
import './user-card.less'
import avator_big from '@/assets/images/avator_big.jpg'
export default {
  name: 'UserCard',
  props: {
    userName: {
      type: String,
      required: true
    },
    loginName: {
      type: String
    },
    userId: {
      type: [Number,String]
    },
    accesses: {
        type: [Array,Object],
        default () {
          return []
        }
    }
  },
  data () {
    return {
      avator_big
    }
  },
  methods: {
      gotoProfile() {
        this.$router.push('profile')
    },
  },
  computed: {
    lastLogin () {
      return this.$store.state.user.lastLogin
    },
  }
}
</script>

<style>

</style>
