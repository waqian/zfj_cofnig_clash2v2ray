# zfj_cofnig_clash2v2ray

# Clash 配置转换工具

这是一个针对 [https://zfj.so](https://zfj.so) 的 Clash 配置转换工具。该工具可以将 Zfj 网站提供的clash订阅链接转换为适用于 v2ray/passwall的配置文件。

## 功能

- 将 Zfj 网站提供的订阅链接（例如： `https://zfj.so/xxxx/clashold`）转换为 v2ray/passwall配置文件。
- 允许用户自定义配置地址（需要手动修改配置文件中的链接）。
- 请手动修改   config_url = "Your_VPN_clash_configuration_url "

- 简化 Clash 配置生成的过程，提高配置管理效率。

## 使用方法

1. **下载项目：**

   克隆该项目到本地：

   ```bash
   git clone https://github.com/waqian/zfj_config_clash2v2ray.git
   cd zfj_config_clash2v2ray
   pip install -r requirements.txt
   python clash_config_all_yaml.py
