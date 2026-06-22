import os
import subprocess
import sys
import time

try:
    import imageio_ffmpeg
except ImportError:
    print("\n[INFO] 'imageio-ffmpeg' is required to combine videos but not found.")
    print("[INFO] Installing 'imageio-ffmpeg' automatically... Please wait.")
    subprocess.run([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"], check=True)
    import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

SCENES = [
    ("Scene 0: Title", "src/scenes/scene_0_title.py", "Scene0Title"),
    ("Scene 1: Introduction", "src/scenes/scene_1_intro.py", "Scene1Intro"),
    ("Scene 2: History", "src/scenes/scene_2_anatomy.py", "Scene2Anatomy"),
    ("Scene 3: System Overview", "src/scenes/scene_3_overview.py", "Scene3Overview"),
    ("Scene 4: Localization", "src/scenes/scene_4_localization.py", "Scene4Localization"),
    ("Scene 5: Normalization", "src/scenes/scene_5_normalization.py", "Scene5Normalization"),
    ("Scene 6: Feature Extraction", "src/scenes/scene_6_feature_extraction.py", "Scene6FeatureExtraction"),
    ("Scene 7: IrisCode Generation", "src/scenes/scene_7_encoding.py", "Scene7Encoding"),
    ("Scene 8: Matching", "src/scenes/scene_8_matching.py", "Scene8Matching"),
    ("Scene 9: Evaluation", "src/scenes/scene_9_evaluation.py", "Scene9Evaluation"),
    ("Scene 10: Modern Methods", "src/scenes/scene_10_modern.py", "Scene10Modern")
]

QUALITIES = {
    "1": ("Low Quality (480p, 15fps) - Fast Preview", "-pql", "480p15"),
    "2": ("Medium Quality (720p, 30fps)", "-pqm", "720p30"),
    "3": ("High Quality (1080p, 60fps) - Standard Full HD", "-pqh", "1080p60"),
    "4": ("4K Quality (2160p, 60fps) - Ultra HD", "-pqk", "2160p60")
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def combine_videos(quality_key):
    folder_res = QUALITIES[quality_key][2]
    concat_list_path = "concat_list.txt"
    output_filename = f"Final_Presentation_{folder_res}.mp4"
    
    print("\n" + "="*50)
    print("COMBINING VIDEOS...")
    print("="*50)
    
    valid_files = []
    for _, file_path, class_name in SCENES:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        video_path = os.path.join(os.getcwd(), "media", "videos", base_name, folder_res, f"{class_name}.mp4")
        
        if os.path.exists(video_path):
            valid_files.append(video_path)
        else:
            print(f"[WARNING] Missing video for {class_name} at {video_path}")
            
    if not valid_files:
        print("\n[ERROR] No rendered videos found for this quality! Please render them first.")
        input("\nPress Enter to return...")
        return
        
    print(f"\nFound {len(valid_files)} rendered scenes. Preparing to merge...")
    
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for vf in valid_files:
            # ffmpeg requires paths to be properly escaped or single quoted in the txt file
            # Format: file 'path'
            escaped_path = vf.replace("'", "'\\''")
            f.write(f"file '{escaped_path}'\n")
            
    cmd_list = [FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", output_filename]
    
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"\n[SUCCESS] Videos successfully combined into: {output_filename}")
        else:
            print(f"\n[ERROR] FFmpeg failed with exit code {result.returncode}")
            print(result.stderr)
    except FileNotFoundError:
        print("\n[ERROR] 'ffmpeg' command not found. Please ensure FFmpeg is installed and in your system PATH.")
    finally:
        if os.path.exists(concat_list_path):
            os.remove(concat_list_path)
            
    input("\nPress Enter to return to main menu...")

def main():
    while True:
        clear_screen()
        print("="*50)
        print("   IRIS RECOGNITION MANIM RENDERER")
        print("="*50)
        print("\n--- Select Rendering Quality ---")
        for key, (desc, _, _) in QUALITIES.items():
            print(f"[{key}] {desc}")
        
        q_choice = input("\nEnter quality choice (1-4) or 'q' to quit: ").strip().lower()
        if q_choice == 'q':
            break
        if q_choice not in QUALITIES:
            print("Invalid choice!")
            time.sleep(1)
            continue
            
        quality_flag = QUALITIES[q_choice][1]

        while True:
            clear_screen()
            print("="*50)
            print(f" Quality Selected: {QUALITIES[q_choice][0]}")
            print("="*50)
            print("\n--- Select Action ---")
            for i, (name, _, _) in enumerate(SCENES):
                print(f"[{i}] {name}")
            print(f"\n[A] RENDER ALL SCENES (0 to {len(SCENES)-1} sequentially)")
            print(f"[AC] RENDER ALL AND AUTO-COMBINE INTO ONE VIDEO")
            print(f"[C] COMBINE ALREADY RENDERED SCENES")
            print(f"[B] Back to Quality Selection")
            
            s_choice = input("\nEnter choice: ").strip().lower()
            if s_choice == 'b':
                break
            
            if s_choice == 'c':
                combine_videos(q_choice)
                continue
                
            scenes_to_render = []
            auto_combine = False
            
            if s_choice == 'a':
                scenes_to_render = SCENES
            elif s_choice == 'ac':
                scenes_to_render = SCENES
                auto_combine = True
            elif s_choice.isdigit() and 0 <= int(s_choice) < len(SCENES):
                scenes_to_render = [SCENES[int(s_choice)]]
            else:
                print("Invalid choice!")
                time.sleep(1)
                continue
                
            print("\n" + "="*50)
            print("STARTING RENDER PROCESS...")
            print("="*50 + "\n")
            
            for name, file_path, class_name in scenes_to_render:
                print(f">>> Rendering {name}...")
                cmd = ["manim", quality_flag, file_path, class_name]
                
                try:
                    result = subprocess.call(cmd)
                    if result != 0:
                        print(f"\n[ERROR] Render failed for {name} (Exit code {result})")
                        input("\nPress Enter to continue...")
                        break
                except FileNotFoundError:
                    print("\n[ERROR] 'manim' command not found. Ensure your virtual environment is activated.")
                    input("\nPress Enter to return to menu...")
                    break
                    
            if len(scenes_to_render) > 1:
                print("\n" + "="*50)
                print("ALL SELECTED SCENES RENDERED SUCCESSFULLY!")
                print("="*50)
                
                if auto_combine:
                    combine_videos(q_choice)
                else:
                    combine_prompt = input("\nDo you want to combine all scenes into a single video now? (y/n): ").strip().lower()
                    if combine_prompt == 'y':
                        combine_videos(q_choice)
                    else:
                        input("\nPress Enter to return to menu...")
            else:
                input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    main()
