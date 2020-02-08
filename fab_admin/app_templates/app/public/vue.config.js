const path = require('path')
const fs = require('fs')
const webpack = require('webpack')
const WebpackShellPlugin = require('webpack-shell-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')

const resolve = dir => {
    return path.join(__dirname, dir)
}

const env = process.env.NODE_ENV || 'development'
fs.writeFileSync(path.join(__dirname, './config/env.js'), `export default '${env}'`)

const BASE_URL = './static/vue/'

module.exports = {
    // Project deployment base
    // By default we assume your app will be deployed at the root of a domain,
    // e.g. https://www.my-app.com/
    // If your app is deployed at a sub-path, you will need to specify that
    // sub-path here. For example, if your app is deployed at
    // https://www.foobar.com/my-app/
    // then change this to '/my-app/'
    baseUrl: process.env.NODE_ENV === 'production' ? BASE_URL : '/',
    outputDir: './dist',
    productionSourceMap: false,
    // tweak internal webpack configuration.
    // see https://github.com/vuejs/vue-cli/blob/dev/docs/webpack.md
    chainWebpack: config => {
        config.resolve.alias
            .set('@', resolve('src'))
            .set('_c', resolve('src/components'))
            .set('_conf', resolve('config'))
        config.module.rule('fonts')
            .test(/\.(woff2?|eot|ttf|otf)(\?.*)?$/i)
            .use('url-loader')
            .loader('url-loader')
            .options({
                name: `fonts/[name].[hash:8].[ext]`,
                publicPath: BASE_URL
            })
    },
    css: {
        extract: true,
    },
    configureWebpack: {
        plugins: [
            new WebpackShellPlugin({
                onBuildStart: [
                    'echo "Deleteing files ... "',
                    'rm -rf ../static/vue/*',
                    'echo "DONE ... "'
                ],
                onBuildEnd: [
                    'echo "Copy files ... "',
                    'cp -r dist/css ../static/vue/',
                    'cp -r dist/img ../static/vue/',
                    'cp -r dist/js ../static/vue/',
                    'cp dist/*.html ../templates/vue/',
                    'echo "DONE ... "'
                ]
            }),
            new CopyWebpackPlugin([{
                    context: './dist',
                    from: '**',
                    to: '../static/vue/',
                    toType: "dir"
                },
                {
                    context: './dist',
                    from: '*.html',
                    to: '../templates/vue/',
                    toType: "file",
                    force: true
                }
            ]),
            new webpack.ProvidePlugin({
                jQuery: "jquery",
                $: "jquery",
                'window.jQuery': "jquery"
            })
        ]
    },
    devServer: {
        port: 8080,
        host: 'localhost',
        contentBase: path.join(__dirname, 'dist'),
    }

}