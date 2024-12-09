const std = @import("std");

const Vec2 = struct { x: i32, y: i32 };

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn set_char(data: [][]u8, pos: Vec2, c: u8) void {
    data[@intCast(pos.y)][@intCast(pos.x)] = c;
}

fn get_char(data: [][]u8, pos: Vec2) u8 {
    return data[@intCast(pos.y)][@intCast(pos.x)];
}

fn print_map(data: [][]u8) void {
    for (data) |line| {
        std.debug.print("{s}\n", .{line});
    }
    std.debug.print("\n", .{});
    return;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var pos: Vec2 = .{ .x = 0, .y = 0 };
    var y_start: i32 = 0;

    var data_ba = std.BoundedArray([]u8, 200){};
    var lines = std.mem.splitSequence(u8, input, "\n");
    while (lines.next()) |line| {
        const line_trimmed = std.mem.trim(u8, line, " \n\r");
        const trimmed_copy = try allocator.dupe(u8, line_trimmed);
        try data_ba.append(trimmed_copy);

        if (std.mem.indexOfAny(u8, line_trimmed, "^>v<")) |x_start| {
            pos = .{ .x = @intCast(x_start), .y = y_start };
        }
        y_start += 1;
    }

    const data: [][]u8 = data_ba.slice();

    //print_map(data);

    //std.debug.print("Pos: {any}\n", .{pos});

    const dirs = [_]Vec2{
        .{ .x = 0, .y = -1 },
        .{ .x = 1, .y = 0 },
        .{ .x = 0, .y = 1 },
        .{ .x = -1, .y = 0 },
    };
    const dir_lut = "^>v<";

    while (true) {
        const cur_c = get_char(data, pos);
        var cur_lut_pos = std.mem.indexOfScalar(u8, dir_lut, cur_c).?;
        var cur_dir = dirs[cur_lut_pos];
        var next: Vec2 = .{ .x = pos.x + cur_dir.x, .y = pos.y + cur_dir.y };

        set_char(data, pos, 'X');

        if (next.x < 0 or next.y < 0 or next.x >= data.len or next.y >= data[0].len)
            break;

        if (get_char(data, next) == '#') {
            cur_lut_pos = (cur_lut_pos + 1) % dir_lut.len;
            cur_dir = dirs[cur_lut_pos];
            next = .{ .x = pos.x + cur_dir.x, .y = pos.y + cur_dir.y };
        }

        set_char(data, next, dir_lut[cur_lut_pos]);
        pos = next;
    }

    //print_map(data);

    var total: usize = 0;
    for (data) |y| {
        total += std.mem.count(u8, y, "X");
    }

    std.debug.print("{d}", .{total});
}
