# config_converter.py
import base64
import json
import urllib.parse
import requests
import yaml


def fetch_clash_config(url):
    """从远程URL获取Clash配置文件"""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return yaml.safe_load(resp.text)
    except requests.exceptions.RequestException as e:
        print(f"配置文件下载失败: {str(e)}")
        exit(1)


def generate_ss_url(proxy):
    """生成SS协议配置"""
    method_passwd = f"{proxy['cipher']}:{proxy['password']}".encode()
    b64_str = base64.urlsafe_b64encode(method_passwd).decode().rstrip('=')
    name_encoded = urllib.parse.quote(proxy['name'], safe='')
    return f"ss://{b64_str}@{proxy['server']}:{proxy['port']}/?group=#{name_encoded}"


def generate_trojan_url(proxy):
    """生成Trojan协议配置"""
    allow_insecure = 1 if proxy.get('skip-cert-verify', False) else 0
    name_encoded = urllib.parse.quote(proxy['name'], safe='')
    params = {
        'allowInsecure': allow_insecure,
        'type': proxy.get('network', 'tcp'),
        'security': 'tls' if proxy.get('tls', False) else 'none',
        'sni': proxy.get('sni', ''),
        'path': urllib.parse.quote(proxy.get('ws-path', ''), safe=''),
        'host': proxy.get('ws-headers', {}).get('Host', ''),
        'serviceName': name_encoded
    }
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v})
    return f"trojan://{proxy['password']}@{proxy['server']}:{proxy['port']}?{query}#{name_encoded}"


def generate_vless_url(proxy):
    """生成VLESS协议配置"""
    flow = proxy.get('flow', 'xtls-rprx-direct')
    security = 'tls' if proxy.get('tls', False) else 'none'
    params = {
        'type': proxy.get('network', 'tcp'),
        'security': security,
        'sni': proxy.get('servername', ''),
        'host': proxy.get('ws-headers', {}).get('Host', ''),
        'path': urllib.parse.quote(proxy.get('ws-path', ''), safe=''),
        'flow': flow,
        'allowInsecure': 1 if proxy.get('skip-cert-verify', False) else 0
    }
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v})
    name_encoded = urllib.parse.quote(proxy['name'], safe='')
    return f"vless://{proxy['uuid']}@{proxy['server']}:{proxy['port']}?{query}#{name_encoded}"


def generate_vmess_url(proxy):
    """生成VMess协议配置"""
    config = {
        "v": "2",
        "ps": proxy['name'],
        "add": proxy['server'],
        "port": str(proxy['port']),
        "id": proxy['uuid'],
        "aid": str(proxy.get('alterId', 0)),
        "scy": proxy.get('cipher', 'auto'),
        "net": proxy.get('network', 'tcp'),
        "type": proxy.get('ws-opts', {}).get('headers', {}).get('type', 'none'),
        "host": proxy.get('ws-opts', {}).get('headers', {}).get('Host', ''),
        "path": proxy.get('ws-path', ''),
        "tls": 'tls' if proxy.get('tls', False) else '',
        "sni": proxy.get('servername', '')
    }
    b64_config = base64.urlsafe_b64encode(json.dumps(config).encode()).decode().rstrip('=')
    return f"vmess://{b64_config}"


def write_config(output_path, content):
    """写入配置文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))


def main():
    config_url = "Your_VPN_clash_configuration_url "

    # 获取并解析配置
    clash_config = fetch_clash_config(config_url)
    proxies = clash_config.get('proxies', [])

    # 初始化分组
    groups = {
        'ss': ['#ss'],
        'trojan': ['\n#trojan'],
        'vless': ['\n#vless'],
        'vmess': ['\n#vmess']
    }

    for p in proxies:
        if p['type'] == 'ss':
            groups['ss'].append(generate_ss_url(p))
        elif p['type'] == 'trojan':
            groups['trojan'].append(generate_trojan_url(p))
        elif p['type'] == 'vless':
            groups['vless'].append(generate_vless_url(p))
        elif p['type'] == 'vmess':
            groups['vmess'].append(generate_vmess_url(p))

    # 合并配置并写入文件
    full_config = []
    for group in groups.values():
        full_config.extend(group)
    write_config('v2ray.conf', full_config)


if __name__ == '__main__':
    main()
