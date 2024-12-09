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
    if (pos.x < 0 or pos.y < 0 or pos.y >= data.len or pos.x >= data[0].len)
        return;

    data[@intCast(pos.y)][@intCast(pos.x)] = c;
}

fn get_char(data: [][]u8, pos: Vec2) ?u8 {
    if (pos.x < 0 or pos.y < 0 or pos.y >= data.len or pos.x >= data[0].len)
        return null;

    return data[@intCast(pos.y)][@intCast(pos.x)];
}

fn print_map(data: [][]u8) void {
    for (data) |line| {
        std.debug.print("{s}\n", .{line});
    }
    std.debug.print("\n", .{});
    return;
}

fn data_to_map(input: []u8, allocator: std.mem.Allocator) ![][]u8 {
    var data_ba = std.BoundedArray([]u8, 500){};
    var lines = std.mem.splitSequence(u8, input, "\n");
    while (lines.next()) |line| {
        const line_trimmed = std.mem.trim(u8, line, " \n\r");
        const trimmed_copy = try allocator.dupe(u8, line_trimmed);
        try data_ba.append(trimmed_copy);
    }

    const data: [][]u8 = data_ba.slice();
    return data;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");
    const map = try data_to_map(input, allocator);

    //print_map(map);

    //Find stations
    var stations = std.AutoHashMap(u8, std.ArrayList(Vec2)).init(allocator);

    for (map, 0..) |line, y| {
        for (line, 0..) |d, x| {
            if (d != '.') {
                if (stations.getPtr(d)) |*l| {
                    try l.*.append(.{ .x = @intCast(x), .y = @intCast(y) });
                } else {
                    var l = std.ArrayList(Vec2).init(allocator);
                    try l.append(.{ .x = @intCast(x), .y = @intCast(y) });
                    try stations.put(d, l);
                }
            }
        }
    }

    var total: i32 = 0;
    var stations_iter = stations.valueIterator();
    while (stations_iter.next()) |station| {
        for (station.items) |a| {
            for (station.items) |b| {
                if (std.meta.eql(a, b))
                    continue;

                const d: Vec2 = .{ .x = a.x - b.x, .y = a.y - b.y };
                var node: Vec2 = .{ .x = a.x, .y = a.y };
                while (true) {
                    const c = get_char(map, node);
                    if (c == null)
                        break;

                    if (c != '#') {
                        total += 1;
                        set_char(map, node, '#');
                    }
                    node = .{ .x = node.x + d.x, .y = node.y + d.y };
                }

                //std.debug.print("{any} -> {any}\n", .{ a, b });
            }
        }

        std.debug.print("\n", .{});
    }

    //print_map(map);
    std.debug.print("{d}", .{total});
}
