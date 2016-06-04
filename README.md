##Purpose
Purpose of the library is to publish output from [checkpatch](https://github.com/torvalds/linux/blob/master/scripts/checkpatch.pl) to a format [jenkins](https://jenkins.io/) understands so that we can take advantage of their tools to publish checkpatch output and continiuos integration becomes easy.

##Approach
We are going to take following approach
* Jenkins have out-of-the-box support for publishing "Junit testcase results". This expects specially formatted xml file as testcase result output. The basic format I found out at this stackoverflow [answer](http://stackoverflow.com/a/9691131)
* Without reinventing the wheel we are going to convert checkpatch output to a xml file equivalent to Junit testcase.
* I am not conversant with all the features of Juint reports. So the xml file generated could be very minimal. Patches/Pull requests for extension are welcome.

## How to run
TODO

