# Makefile for tinymce
all: tinymce

tinymce_zip = tinymce_3.4.9_jquery.zip

tinymce:
	wget http://github.com/downloads/tinymce/tinymce/$(tinymce_zip)
	unzip $(tinymce_zip)
	rm -rf static/js/tiny_mce
	mv tinymce/jscripts/tiny_mce static/js
	rm -rf $(tinymce_zip) tinymce
