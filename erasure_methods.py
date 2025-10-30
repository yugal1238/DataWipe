import os, random

def wipe(file_path, passes, progress, mode):
    size = os.path.getsize(file_path)
    with open(file_path, "r+b") as f:
        for p in range(passes):
            f.seek(0)
            for _ in range(size):
                if mode == "zero":
                    f.write(b"\x00")
                else:
                    f.write(bytes([random.randint(0, 255)]))
            f.flush()
            progress.set((p + 1) / passes)

def wipe_file_zero_pass(path, progress):
    wipe(path, 1, progress, "zero")

def wipe_file_random_pass(path, progress):
    wipe(path, 1, progress, "random")

def wipe_file_dod_three_pass(path, progress):
    wipe(path, 3, progress, "random")
