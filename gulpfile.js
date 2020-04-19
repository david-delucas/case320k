var gulp = require("gulp");
var browserify = require("browserify");
var source = require('vinyl-source-stream');
var tsify = require("tsify");


var build = function(cfg) {
    return browserify({
        basedir: './client/src',
        debug: cfg.debug,
        entries: ['index.ts'],
        cache: {},
        packageCache: {}
    })
    .plugin(tsify)
    .bundle()
    .pipe(source('app.js'))
    .pipe(gulp.dest("case320k/static/assets"));
}


gulp.task("debug", function () {
    return build({debug: true,ignore: ["./node_modules","./case320k"]})
});


gulp.task("build", function () {
    return build({debug: false,ignore: ["./node_modules","./case320k"]})
});


gulp.task("watch", function () {
    gulp.watch(['client/src/**/*.ts'], ['debug']);
});

gulp.task("default", ["debug"], function() {
    gulp.start('watch')
});