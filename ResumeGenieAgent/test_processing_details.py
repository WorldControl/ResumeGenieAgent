#!/usr/bin/env python3
"""
测试处理详情返回功能
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_search_jobs_with_details():
    """测试岗位搜索接口的处理详情"""
    print("=== 测试岗位搜索处理详情 ===")
    
    try:
        data = {
            "job_title": "数据分析师",
            "location": "北京"
        }
        
        print(f"发送请求: {json.dumps(data, ensure_ascii=False)}")
        response = requests.post(f"{BASE_URL}/search_jobs", json=data)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ 请求成功！")
            print(f"找到岗位数量: {result.get('total_count', 0)}")
            print(f"总处理时间: {result.get('total_processing_time', 0):.2f}秒")
            
            print(f"\n📊 处理详情:")
            for i, step in enumerate(result.get('processing_details', []), 1):
                print(f"\n步骤 {i}: {step['step_name']}")
                print(f"  状态: {step['status']}")
                print(f"  消息: {step['message']}")
                if step.get('execution_time'):
                    print(f"  执行时间: {step['execution_time']:.3f}秒")
                if step.get('details'):
                    print(f"  详情: {json.dumps(step['details'], ensure_ascii=False, indent=4)}")
            
            return True
        else:
            print(f"❌ 请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_health():
    """测试健康检查"""
    print("=== 测试健康检查 ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ 服务正常: {response.json()}")
            return True
        else:
            print(f"❌ 服务异常: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试处理详情功能...")
    
    # 检查服务是否运行
    if not test_health():
        print("❌ 服务未启动，请先启动服务")
        return
    
    print("\n" + "="*50)
    
    # 测试岗位搜索
    success = test_search_jobs_with_details()
    
    print("\n" + "="*50)
    if success:
        print("🎉 所有测试通过！处理详情功能正常工作")
    else:
        print("❌ 测试失败，请检查服务状态")

if __name__ == "__main__":
    main()
