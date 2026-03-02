import pandas as pd

capture_frame = pd.read_csv('./generated/capture.csv')

located_src = []
located_dst = []
located_id = []


print(capture_frame)

for x in capture_frame.index:
    if capture_frame.loc[x, "src"] not in located_src:
        located_src.append(capture_frame.loc[x, "src"])
        capture_frame.loc[x, "src"] = located_src.index(capture_frame.loc[x, "src"])
    elif capture_frame.loc[x, "src"] in located_src:
        capture_frame.loc[x, "src"] = located_src.index(capture_frame.loc[x, "src"])

    if capture_frame.loc[x, "dst"] not in located_dst:
        located_dst.append(capture_frame.loc[x, "dst"])
        capture_frame.loc[x, "dst"] = located_dst.index(capture_frame.loc[x, "dst"])
    elif capture_frame.loc[x, "dst"] in located_dst:
        capture_frame.loc[x, "dst"] = located_dst.index(capture_frame.loc[x, "dst"])
        
capture_frame.drop('payload', inplace=True, axis=1)
        
print("changed to")
print(capture_frame)

print("located SRC:")
print(located_src)

print("located DST:")
print(located_dst)

capture_frame.to_csv("./generated/formatted_capture.csv", index=False)


