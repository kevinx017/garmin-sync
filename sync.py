from garminconnect import Garmin
import os

# 从环境变量读取账号（安全不泄露）
INTL_EMAIL = os.getenv("GARMIN_INTL_EMAIL")
INTL_PWD = os.getenv("GARMIN_INTL_PASSWORD")
CN_EMAIL = os.getenv("GARMIN_CN_EMAIL")
CN_PWD = os.getenv("GARMIN_CN_PASSWORD")

def main():
    print("🔗 登录佳明国际版...")
    intl = Garmin(INTL_EMAIL, INTL_PWD, is_cn=False)
    intl.login()

    print("🔗 登录佳明大陆版...")
    cn = Garmin(CN_EMAIL, CN_PWD, is_cn=True)
    cn.login()

    # 获取最近7天的活动
    print("📥 获取国际版活动...")
    activities = intl.get_activities(limit=7)

    sync_count = 0
    for act in activities:
        act_id = act["activityId"]
        name = act["activityName"]
        print(f"正在处理: {name} ({act_id})")

        try:
            # 下载.fit原始数据
            fit_data = intl.download_activity(act_id, fmt="fit")

            # 上传大陆版
            cn.upload_activity(
                activity_data=fit_data,
                activity_name=name,
                activity_type=act["activityType"]["typeKey"],
                detect_duplicates=True  # 自动去重
            )
            print(f"✅ 同步成功: {name}")
            sync_count += 1
        except Exception as e:
            if "duplicate" in str(e).lower():
                print(f"ℹ️ 已存在，跳过: {name}")
            else:
                print(f"❌ 失败: {name} | {str(e)}")

    print(f"\n🎉 同步完成！本次成功同步: {sync_count} 条")

if __name__ == "__main__":
    main()
