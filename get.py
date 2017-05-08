import ssl
import socket


class Get():
    def parsed_url(self, url):
        """
        解析 url 返回 (protocol host port path)
        有的时候有的函数, 它本身就美不起来, 你要做的就是老老实实写
        """
        # 检查协议
        protocol = 'http'
        if url[:7] == 'http://':
            u = url.split('://')[1]
        elif url[:8] == 'https://':
            protocol = 'https'
            u = url.split('://')[1]
        else:
            # '://' 定位 然后取第一个 / 的位置来切片
            u = url

        # 检查默认 path
        i = u.find('/')
        if i == -1:
            host = u
            path = '/'
        else:
            host = u[:i]
            path = u[i:]

        # 检查端口
        port_dict = {
            'http': 80,
            'https': 443,
        }
        # 默认端口
        port = port_dict[protocol]
        if host.find(':') != -1:
            h = host.split(':')
            host = h[0]
            port = int(h[1])

        return protocol, host, port, path


    def socket_by_protocol(self, protocol):
        """
        根据协议返回一个 socket 实例
        """
        if protocol == 'http':
            s = socket.socket()
        else:
            # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
            # 除此之外无其他差别
            s = ssl.wrap_socket(socket.socket())
        return s


    def response_by_socket(self, s):
        """
        参数是一个 socket 实例
        返回这个 socket 读取的所有数据
        """
        response = b''
        buffer_size = 1024
        while True:
            r = s.recv(buffer_size)
            if len(r) == 0:
                break
            response += r
        return response


    def parsed_response(self, r):
        """
        把 response 解析出 状态码 headers body 返回
        状态码是 int
        headers 是 dict
        body 是 str
        """
        header, body = r.split('\r\n\r\n', 1)
        h = header.split('\r\n')
        status_code = h[0].split()[1]
        status_code = int(status_code)

        headers = {}
        for line in h[1:]:
            k, v = line.split(': ')
            headers[k] = v
        return status_code, headers, body


    # 复杂的逻辑全部封装成函数
    def get(self, url):
        """
        用 GET 请求 url 并返回响应
        """
        protocol, host, port, path = self.parsed_url(url)

        s = self.socket_by_protocol(protocol)
        s.connect((host, port))

        request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
        encoding = 'utf-8'
        s.send(request.encode(encoding))

        response = self.response_by_socket(s)
        r = response.decode(encoding)

        status_code, headers, body = self.parsed_response(r)
        if status_code == 301:
            url = headers['Location']
            return self.get(url)

        return status_code, headers, body

if __name__ == '__main__':
    get = Get()