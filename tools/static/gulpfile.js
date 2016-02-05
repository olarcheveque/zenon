var gulp       = require('gulp'),
    sass       = require('gulp-sass'),
    path       = require('path');

// display (or swallow?) an error in console
// also prevent error to stop the gulp watch process unless restart
function swallowError (error) {
  console.log(error.toString());
  this.emit('end');
};

gulp.task('sass', function() {
  return gulp.src('../../erudit/base/static/sass/main.scss')
    .pipe(sass())
    .on('error', sass.logError)
    .pipe(gulp.dest('../../erudit/base/static/css/'));
});

gulp.task('watch', function() {
  // watch any less file /css directory, ** is for recursive mode
  gulp.watch('../../erudit/base/static/sass/**/*.scss', ['sass']);
});