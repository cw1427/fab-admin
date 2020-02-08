<template>
<Row>
    <Col span='24'>
    <div class="profile-form" v-if="items.length">
        <div class="profile-user-info profile-user-info-striped">
            <div class="profile-info-row" v-for="item in items"> 
                <div class="profile-info-name">{{item.name}}</div>
                <template v-if="item.renderComponent">
                    <div  class="profile-info-value">
                        <component :is="item.renderComponent"></component>
                    </div>
                </template>
                <template v-else>
                    <div class="profile-info-value " v-html="item.value"></div>
                </template>
            </div>
            <div class="profile-info-row" v-if="tableColumnsFilters && tableColumnsFilters.length>0"> 
                <div class="profile-info-name">filter</div>
                <div class="profile-info-value " >
                    <Table
                    border
                    :data="filters"
                    :columns="tableColumnsFilters"
                    stripe
                    @on-sort-change="sortChange">
                    </Table>
                </div>
            </div>
        </div>
    </div>
    <div class="" style="margin-top:2px; margin: 0 12px;">
            <Table
            :loading="loading"
            :highlight-row="highlight"
            border
            :data="data"
            :columns="tableColumns"
            @on-sort-change="sortChange"
            stripe>
            </Table>
        <div style="margin: 10px;overflow: hidden">
          <div style="float: right;">
              <Page :total="total" :current="currentPage" show-sizer show-total :page-size="pageSize" :page-size-opts="[1,10,20,50,100]" 
                @on-change="onChange" @on-page-size-change="onPageSizeChange"></Page>
          </div>
        </div>
    </div>

    </Col>
</Row>

</template>

<script>
import './history-table.less'
import Vue from 'vue'
export default {
    name: "HistoryTable",
    props: [
      'items',//profile form item list
      'target',
      'columns',//columns description Obj
      'data',   //table data
      'search',  // filter searching Obj
      'loading',
      'highlight',
      'total',
      'currentPage',
      'pageSize'
    ],
    data() {
      return {
          filters: [{
            title: ''
          }],
          tableColumns:[],
          tableColumnsFilters:[]
      }
    },
    created() {

        for (let index in this.columns) {
            if (this.columns[index].hide){
                continue
            }
            this.tableColumns.push(this.columns[index])
            if (this.columns[index].filter) {
                let filter = {}
                this.$set(filter, 'title', this.columns[index].title);
                this.$set(filter, 'key', this.columns[index].key);
                let render = (h) => {
                };
                //---select filter
                if (this.columns[index].filter.type && this.columns[index].filter.type === 'Select') {
                    this.$set(filter, 'width', '200');
                    render = (h) => {
                    return h(this.columns[index].filter.type, {
                        props: {
                        value:-1
                        },
                        on: {
                        'on-change': (val) => {
                            this.value=val
                            if (val === 0) {
                            this.$delete(this.search, this.columns[index].key);
                            this.load();
                            return;
                            }
                            this.$set(this.search, this.columns[index].key, val);
                            this.load();
                        }
                        }
                    }, this.createOptionsRender(index, h));
                    }
                } else {
                    //---input filter
                    this.$set(filter, 'width', '150');
                    render = (h) => {
                    let inputValue = null;
                    return h(this.columns[index].filter.type, {
                        props: {
                        placeholder: 'Input ' + this.columns[index].title,
                        icon: 'ios-search-strong'
                        },
                        on: {
                        input: val => {
                            inputValue = val;
                            if (!inputValue) {
                            this.validInputValue(index, inputValue);
                            }
                        },
                        'on-click': (event) => {
                            this.validInputValue(index, inputValue);
                        },
                        'on-enter': (event) => {
                            inputValue = event.target.value;
                            this.validInputValue(index, inputValue);
                        }
                        }
                    })
                    };
                }
                this.$set(filter, 'render', render);
                this.tableColumnsFilters.push(filter);
            }
        }
    },
    methods: {
      load() {
        this.$emit('load',true);
      },
      validInputValue(index, inputValue) {
        if (!inputValue) {
          this.$delete(this.search, this.columns[index].key);
          this.load();
          return;
        }
        this.$set(this.search, this.columns[index].key, inputValue);
        this.load();
      },
      onChange (c) {
          this.$emit('onChange',c)
      },
      sortChange (c) {
          this.$emit('sortChange',c)
      },
      onPageSizeChange (c) {
          this.$emit('onPageSizeChange',c)
      }
    }
}
</script>

<style scoped>
</style>