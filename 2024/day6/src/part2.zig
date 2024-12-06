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

fn test_route(data: [][]u8, start: Vec2) bool {
    const dirs = [_]Vec2{
        .{ .x = 0, .y = -1 },
        .{ .x = 1, .y = 0 },
        .{ .x = 0, .y = 1 },
        .{ .x = -1, .y = 0 },
    };
    const dir_lut = "^>v<";

    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const key_t = struct { b: Vec2, p: Vec2, d: Vec2 };
    var det = std.AutoHashMap(key_t, bool).init(allocator);
    defer det.deinit();

    var pos = start;
    while (true) {
        var cur_c = get_char(data, pos);
        const cur_lut_pos_t = std.mem.indexOfScalar(u8, dir_lut, cur_c);
        if (cur_lut_pos_t == null)
            std.debug.print("{c}\n", .{cur_c});

        var cur_lut_pos = cur_lut_pos_t.?;

        var cur_dir = dirs[cur_lut_pos];
        var next: Vec2 = .{ .x = pos.x + cur_dir.x, .y = pos.y + cur_dir.y };

        //set_char(data, pos, 'X');

        if (next.x < 0 or next.y < 0 or next.x >= data.len or next.y >= data[0].len)
            return true;

        if (get_char(data, next) == '#') {
            const t: key_t = .{ .b = next, .d = cur_dir, .p = pos };
            if (det.contains(t))
                return false;

            det.put(t, true) catch {};

            cur_lut_pos = (cur_lut_pos + 1) % dir_lut.len;
            cur_dir = dirs[cur_lut_pos];
            next = pos;
            cur_c = dir_lut[cur_lut_pos];
        }

        set_char(data, next, cur_c);
        pos = next;
    }

    return false;
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
        if (line_trimmed.len > 0) {
            const trimmed_copy = try allocator.dupe(u8, line_trimmed);
            try data_ba.append(trimmed_copy);
        }

        if (std.mem.indexOfAny(u8, line_trimmed, "^>v<")) |x_start| {
            pos = .{ .x = @intCast(x_start), .y = y_start };
        }
        y_start += 1;
    }

    const data: [][]u8 = data_ba.slice();

    var test_pos = std.ArrayList(Vec2).init(allocator);
    defer test_pos.deinit();
    {
        const data_copy: [][]u8 = try allocator.dupe([]u8, data);
        defer allocator.free(data_copy);
        for (data_copy) |*d| {
            d.* = try allocator.dupe(u8, d.*);
        }

        _ = test_route(data_copy, pos);
        //print_map(data_copy);

        for (0..(data.len)) |y| {
            for (0..(data[0].len)) |x| {
                const t_pos: Vec2 = .{ .x = @intCast(x), .y = @intCast(y) };
                if (std.mem.indexOfScalar(u8, "^>v<", get_char(data_copy, t_pos)) != null) {
                    if (!std.meta.eql(t_pos, pos))
                        try test_pos.append(t_pos);
                }
            }
        }
    }

    const test_slice = try test_pos.toOwnedSlice();
    //std.debug.print("{d}\n", .{test_slice.len});

    var total: usize = 0;
    for (test_slice) |test_p| {
        const data_copy: [][]u8 = try allocator.dupe([]u8, data);
        defer allocator.free(data_copy);
        for (data_copy) |*d| {
            d.* = try allocator.dupe(u8, d.*);
        }

        set_char(data_copy, test_p, '#');

        if (!test_route(data_copy, pos))
            total += 1;
    }

    std.debug.print("{d}", .{total});
}
