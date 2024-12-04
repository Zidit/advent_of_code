const std = @import("std");

const Vec2 = struct { x: i32, y: i32 };

fn read_input() ![]u8 {
    const file = try std.fs.cwd().openFile("src/input.txt", .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn search(data: [][]const u8, str: []const u8, pos: Vec2, dir: Vec2) bool {
    if (str.len == 0)
        return true;

    if (pos.x < 0 or pos.y < 0 or pos.x >= data[0].len or pos.y >= data.len)
        return false;

    if (data[@intCast(pos.y)][@intCast(pos.x)] != str[0])
        return false;

    return search(data, str[1..], .{ .x = pos.x + dir.x, .y = pos.y + dir.y }, dir);
}

pub fn main() !void {
    const input = try read_input();
    //const input =
    //    \\MMMSXXMASM
    //    \\MSAMXMSMSA
    //    \\AMXSXMAAMM
    //    \\MSAMASMSMX
    //    \\XMASAMXAMM
    //    \\XXAMMXXAMA
    //    \\SMSMSASXSS
    //    \\SAXAMASAAA
    //    \\MAMMMXMMMM
    //    \\MXMXAXMASX
    //;

    var data_ba = std.BoundedArray([]const u8, 200){};
    var lines = std.mem.splitSequence(u8, input, "\n");
    while (lines.next()) |line| {
        try data_ba.append(std.mem.trim(u8, line, " \n\r"));
    }

    const data = data_ba.slice();

    const dirs = [_]Vec2{
        .{ .x = 1, .y = 0 },
        .{ .x = 0, .y = 1 },
        .{ .x = 1, .y = 1 },
        .{ .x = -1, .y = 1 },
        .{ .x = 1, .y = -1 },
        .{ .x = -1, .y = -1 },
        .{ .x = 0, .y = -1 },
        .{ .x = -1, .y = 0 },
    };

    var xmas_total: u32 = 0;

    for (0..data.len) |y| {
        for (0..data[0].len) |x| {
            for (dirs) |dir| {
                if (search(data, "XMAS", .{ .x = @intCast(x), .y = @intCast(y) }, dir)) {
                    xmas_total += 1;
                }
            }
        }
    }

    std.debug.print("{any}\n", .{xmas_total});
}
