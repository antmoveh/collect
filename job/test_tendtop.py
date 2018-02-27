from job.tendtop import *


itr = interceptor()

index = itr.tank_process([3, 1, 'W'])
itr.output(index)
index = itr.tank_process([11, 39, 'w', 'MTMPRPMTMLMRPRMTPLMMTLMRRMP'])
itr.output(index)
index = itr.tank_process(['2', '3', 'e', 'MTMPRPMTMLMRPffsfefsMRRMP'])
itr.output(index)
index = itr.tank_process(['2', 36, 's', 'MTMPRPMTMLMRPRMTPLMMTLMRRMP'])
itr.output(index)
index = itr.tank_process(['b', 36, 'S', 'MTMPRPMTMLMRPRMTPLMMTLMRRMP'])
itr.output(index)
index = itr.tank_process(['c', 'aa', 's', 'MTMPRPMTMLMRPffsfefsMRRMP'])
itr.output(index)
print('*'*50)
itr.output('all')
print('*'*50)
itr.destroy_tank(3, 1)
itr.output('all')
print('*'*50)
itr.intercept()