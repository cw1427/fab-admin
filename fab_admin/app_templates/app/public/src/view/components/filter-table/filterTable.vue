<template>
  <div>
    <Table
      border
      :data="filters"
      :columns="tableColumnsFilters"
      stripe
      @on-sort-change="sortChange">
    </Table>

    <Table ref="bodyTable"
      :loading="loading"
      :show-header=false
      :highlight-row="highlight"
      border
      :data="data"
      :columns="tableColumns"
      stripe>
    </Table>
  </div>
</template>

<script>
import mixin from './editableMixin.js'
  export default {
    name: "FilterTable",
    mixins: [mixin],
    props: [
      'columns',//columns description Obj
      'data',   //table data
      'search',  // filter searching Obj
      'loading',
      'highlight',
      'showRowNum'
    ],
    data() {
      return {
        filters: [{
          title: ''
        }],
        tableColumnsFilters: [],
        tableColumns: [],
        selects:[],
        checkAll:false
      }
    },
    created() {
      for (let index in this.columns) {
        let filter = {};
        if (this.columns[index].hide){
          continue
        }else if (this.columns[index].type && this.columns[index].type == 'index'){
          if (this.showRowNum){
            this.tableColumns.push(this.columns[index])
          }else{
            continue
          }
        }else{
          this.tableColumns.push(this.columns[index])
        }
        this.$set(filter, 'title', this.columns[index].title);
        this.$set(filter, 'key', this.columns[index].key);
        if (this.columns[index].width) {
          this.$set(filter, 'width', this.columns[index].width);
        }
        if (this.columns[index].sortable){
          this.$set(filter, 'sortable', this.columns[index].sortable);
        }
        let render = (h) => {
        };

        if (this.columns[index].filter) {
          //---select filter
          if (this.columns[index].filter.type && this.columns[index].filter.type === 'Select') {
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
        } else if (this.columns[index].type == 'selection'){
          //----check box render a checkbox in the header table.
          render = (h) => {
            return  h('Row', {}, [ h('Col', {props:{span:12}}, [h('Checkbox',{props: {value:this.checkAll},on:{
                  'on-change': (e) =>{
                      this.checkAll = e
                      this.$refs.bodyTable.selectAll(e);
                  }
              }})]),
                 h('Col',{props:{span:12}}, [h('tooltip',{
                      props: {
                              content: 'Batch delete',
                              placement: 'top'
                          }
                      },[h('Poptip', {
                          props: {
                              confirm: true,
                              title: 'Batch delete all selected?',
                              transfer:true
                          },
                          on: {
                              'on-ok': () => {
                              this.handleBatchDelete()
                              }
                          }   
                      },[h('Button', {
                          props: {
                              type: 'error',
                              size: 'small',
                              icon: 'md-trash',
                              placement: 'top'
                          },
                          style: {
                          }
                          }, '')]
                      )])])
              ]);
          }
        }
        this.$set(filter, 'render', render);
        this.tableColumnsFilters.push(filter);
      }
      // renderEditable(this)
    },
    methods: {
      createOptionsRender(index, h) {
        let optionRender = [];
        if (this.columns[index].filter.option) {
          let option = this.columns[index].filter.option;
          for (let i in option) {
            optionRender.push(h('Option', {
              props: {
                value: option[i].value
              }
            }, option[i].name))
          }
        }
        return optionRender;
      },
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
      sortChange (c) {
          this.$emit('sortChange',c)
      },
      handleBatchDelete(){
        let selects = this.$refs.bodyTable.getSelection()
        if (selects.length == 0){
          this.$Message.warning('Please select at least one item')
        }else{
          let ids=[]
          selects.forEach(item =>{ids.push(item['id'])})
          this.$emit('batchDelete',ids)
        }
      }

    }
  }
</script>

<style scoped>
</style>