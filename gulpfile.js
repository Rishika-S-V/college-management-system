const { src, dest, watch } = require('gulp');
const minifyJs = require("gulp-uglify");
const concat = require("gulp-concat");

const bundleJs = () => {
    return src("./static_src/js/**/*.js")
    .pipe(concat('index.js'))
    .pipe(minifyJs())
    .pipe(dest("./website/static/"));
}

const devWatch = () => {
    watch("./static_src/js/**/*.js", bundleJs);
}

exports.bundleJs = bundleJs;
exports.devWatch = devWatch;
