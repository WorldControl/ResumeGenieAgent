#!/usr/bin/env python3
"""
API测试脚本
"""
import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """测试健康检查接口"""
    print("=== 测试健康检查 ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_search_jobs():
    """测试岗位搜索接口"""
    print("\n=== 测试岗位搜索 ===")
    try:
        data = {
            "job_title": "数据分析师",
            "location": "北京"
        }
        response = requests.post(f"{BASE_URL}/search_jobs", json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_upload_resume():
    """测试简历上传接口"""
    print("\n=== 测试简历上传 ===")
    try:
        # 创建一个测试简历文件
        test_resume_content = """
张三
教育背景：北京大学 计算机科学 本科
工作经验：3年数据分析经验
技能：Python, SQL, Tableau, 机器学习
项目：用户行为分析系统，提升转化率15%
        """
        
        # 保存为临时文件
        with open("test_resume.txt", "w", encoding="utf-8") as f:
            f.write(test_resume_content)
        
        # 上传文件
        with open("test_resume.txt", "rb") as f:
            files = {"file": ("test_resume.txt", f, "text/plain")}
            params = {"job_title": "数据分析师"}
            response = requests.post(f"{BASE_URL}/upload_resume", files=files, params=params)
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        # 清理临时文件
        os.remove("test_resume.txt")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def main():
    """主测试函数"""
    print("开始API测试...")
    
    # 检查服务是否运行
    if not test_health():
        print("❌ 服务未启动或健康检查失败")
        return
    
    # 测试各个接口
    tests = [
        ("健康检查", test_health),
        ("岗位搜索", test_search_jobs),
        ("简历上传", test_upload_resume),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"测试: {test_name}")
        print('='*50)
        success = test_func()
        results.append((test_name, success))
        print(f"{'✅ 通过' if success else '❌ 失败'}")
    
    # 总结
    print(f"\n{'='*50}")
    print("测试总结:")
    print('='*50)
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\n总计: {passed}/{total} 个测试通过")

if __name__ == "__main__":
    main()
