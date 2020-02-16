import camelCase from 'lodash/camelCase'
// Storing in variable a context with all files in this folder
// ending with `.js`.
const requireModule = require.context('.', false, /\.js$/)
const modules = {}

requireModule.keys().forEach(fileName => {
    if (fileName === './index.js') return
    // filter fullstops and extension
  // and return a camel-case name for the file
    const moduleName = camelCase(
        fileName.replace(/(\.\/|\.js)/g, '')
    )
  // create a dynamic object with all modules
    modules[moduleName] = {
           // add namespace here
           namespaced: false,
           ...requireModule(fileName).default
       // if you have exported the object with name in the module `js` file
       // e.g., export const name = {};
       // uncomment this line and comment the above
           // ...requireModule(fileName)[moduleName]
       }
})
// import fab_admin_addon store_module
config.fabadmin_addons.forEach((v)=>{
    try{
        const storeModule = require('#/'+v+'/public/viewui/store.js')
        modules[camelCase(v)] ={ ...storeModule.default }
    }catch(err){

    }
})
export default modules
