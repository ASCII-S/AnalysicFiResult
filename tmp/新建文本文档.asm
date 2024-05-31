mov	0x24(%rsp),%edx
mov	%rax,%r12
xor		%eax,%eax
test		%edx,%edx
jle		400a08 
nopl 	0x0(%rax)
movl 	$0xffffffff,(%r12,%rax,4)	;4009f8
add		$0x1,%rax
cmp 	%eax,%edx
jg 		4009f8
movslq	0x2c(%rsp),%rax	;400a08
mov	$0x400ca6,%edi
movl 	$0x0,(%r12,%rax,4)