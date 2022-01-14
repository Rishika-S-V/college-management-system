const { src, dest, watch } = require('gulp');
const minifyJs = require("gulp-uglify");
const concat = require("gulp-concat");
const babel = require("gulp-babel");

const bundleJs = () => {
    return src("./website/static/src/js/**/*.js")
    .pipe(concat('index.js'))
    .pipe(babel({
        presets: ["@babel/preset-env"]
      }))
    .pipe(minifyJs())
    .pipe(dest("./website/static/dist/"));
}

const devWatch = () => {
    watch("./website/static/src/js/**/*.js", bundleJs);
}

exports.bundleJs = bundleJs;
exports.devWatch = devWatch;
