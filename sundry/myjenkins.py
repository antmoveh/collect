import jenkins, time, json


# jenkins_server_url = 'http://192.168.0.154:8080/'
jenkins_user = 'admin'
jenkins_password = 'admin'

jenkins_server_url = 'http://192.168.0.113:8080/'
# jenkins_user = 'admin'
# jenkins_password = 'admin'

# jenkins.auth_headers(username=jenkins_user, password=jenkins_password)
jenkins_server = jenkins.Jenkins(url=jenkins_server_url, username=jenkins_user, password=jenkins_password, timeout=30)

# last_build_number = jenkins_server.get_job_info('androidtest')['nextBuildNumber']
# print(last_build_number)
# build_info = jenkins_server.get_build_console_output('androidtest', last_build_number)
# print(build_info.encode('utf-8'))
# build_dict = {'module': '排期模块', 'pom': 'cias-base/pom.xml', 'project': 'model', 'git_file': '/cias-base', 'version': '1.0.0', 'order': 1, 'package_type': '.jar', 'timed_task': 'package_version-SNAPSHOT.jar', 'git': 'http://git.kokozu.net/zhangkaixiang/cias-projects.git', 'maven': '-U clean timed_task -Dmaven.test.skip=true -X', 'branch': 'master'}
# jenkins_server.build_job(name='model', parameters=build_dict)
# jenkins_server.copy_job('plans', 'mytest')
# jenkins_server.enable_job('mytest')
# b = jenkins_server.get_job_config('test')
# c = jenkins_server.reconfig_job('mytest2', b)
# with open('E:\\pyworkspace\\auto_build\\conf_temp\\jar_model.xml', 'r', encoding='utf-8') as f:
#     jenkins_server.create_job('test_jar', f.read().replace('JENKINS_GIT_USER', 'fe9ee9fe-62c6-41e8-99de-f400fda5630f'))
view = jenkins_server.get_views()
# print(jenkins_server.view_exists('All'))
try:
    result = jenkins_server.get_build_info(name='cias-uop1_war', number=6)['result']
    print(result)
except jenkins.NotFoundException:
    print(11)