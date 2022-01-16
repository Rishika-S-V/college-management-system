const { src, dest, watch } = require('gulp');
const minifyJs = require("gulp-uglify");
const concat = require("gulp-concat");
const babel = require("gulp-babel");

const bundleCore = () => {
    return src("./website/static/src/js/core/**/*.js")
    .pipe(concat('core.js'))
    .pipe(babel({
        presets: ["@babel/preset-env"]
        }))
    .pipe(minifyJs())
    .pipe(dest("./website/static/dist/js/"));
}

const bundleUi = () => {
    return src("./website/static/src/js/ui/**/*.js")
    .pipe(babel({
        presets: ["@babel/preset-env"]
        }))
    .pipe(minifyJs())
    .pipe(dest("./website/static/dist/js/ui/"));
}

async function bundleJs () {
    await bundleCore();
    await bundleUi();
}

const devWatch = () => {
    watch("./website/static/src/js/**/*.js", bundleJs);
}

exports.default = bundleJs;
exports.watch = devWatch;
