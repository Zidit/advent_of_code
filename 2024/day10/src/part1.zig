const std = @import("std");

const Vec2 = struct { x: i32, y: i32 };
const Map = struct { data: []u8, h: usize, w: usize };

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn map_set(map: Map, pos: Vec2, c: u8) void {
    if (pos.x < 0 or pos.y < 0 or pos.y >= map.h or pos.x >= map.w)
        return;

    const x: usize = @intCast(pos.x);
    const y: usize = @intCast(pos.y);
    map.data[y * map.w + x] = c;
}

fn map_get(map: Map, pos: Vec2) ?u8 {
    if (pos.x < 0 or pos.y < 0 or pos.y >= map.h or pos.x >= map.w)
        return null;

    const x: usize = @intCast(pos.x);
    const y: usize = @intCast(pos.y);
    return map.data[y * map.w + x];
}

fn map_inc(map: Map, pos: Vec2) !void {
    if (pos.x < 0 or pos.y < 0 or pos.y >= map.h or pos.x >= map.w)
        return error.OutOfRange;

    const x: usize = @intCast(pos.x);
    const y: usize = @intCast(pos.y);
    map.data[y * map.w + x] += 1;
}

fn print_map(map: Map) void {
    for (0..map.h) |y| {
        const line = map.data[y * map.w .. (y + 1) * map.w];
        std.debug.print("{s}\n", .{line});
    }
    std.debug.print("\n", .{});
    return;
}

fn print_map_d(map: Map) void {
    for (0..map.h) |y| {
        const line = map.data[y * map.w .. (y + 1) * map.w];
        for (line) |value| {
            std.debug.print("{d} ", .{value});
        }
        std.debug.print("\n", .{});
    }
    std.debug.print("\n", .{});
    return;
}

fn find_from_map(map: Map, needle: u8, allocator: std.mem.Allocator) ![]Vec2 {
    var results = std.ArrayList(Vec2).init(allocator);
    defer results.deinit();

    for (0..map.h) |y| {
        const line = map.data[y * map.w .. (y + 1) * map.w];
        var pos: usize = 0;

        while (std.mem.indexOfScalarPos(
            u8,
            line,
            pos,
            needle,
        )) |index| {
            try results.append(.{ .x = @intCast(index), .y = @intCast(y) });
            pos = index + 1;
        }
    }

    return results.toOwnedSlice();
}

fn data_to_map(input: []u8, allocator: std.mem.Allocator) !Map {
    var data = std.ArrayList(u8).init(allocator);
    var height: usize = 0;
    var width: usize = 0;

    var lines = std.mem.splitSequence(u8, input, "\n");
    while (lines.next()) |line| {
        const line_trimmed = std.mem.trim(u8, line, " \n\r");
        if (width == 0) {
            width = line_trimmed.len;
        } else if (width != line_trimmed.len) {
            return error.OutOfRange;
        }

        try data.appendSlice(line_trimmed);
        height += 1;
    }

    return .{ .data = try data.toOwnedSlice(), .h = height, .w = width };
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");
    const map = try data_to_map(input, allocator);
    defer allocator.free(map.data);

    //print_map(map);

    const ends = try find_from_map(map, '9', allocator);
    defer allocator.free(ends);

    //for (ends) |end|
    //    std.debug.print("{d}, {d}\n", .{ end.x, end.y });

    const route_map = .{ .data = try allocator.alloc(u8, map.h * map.w), .h = map.h, .w = map.w };
    defer allocator.free(route_map.data);
    @memset(route_map.data, 0);

    for (ends) |end| {
        var visited = std.AutoHashMap(Vec2, bool).init(allocator);
        defer visited.deinit();

        var queue = std.ArrayList(Vec2).init(allocator);
        defer queue.deinit();

        try queue.append(end);

        while (queue.items.len > 0) {
            const current = queue.pop();

            if (visited.contains(current))
                continue;

            try visited.put(current, true);
            try map_inc(route_map, current);

            const next = [_]Vec2{
                .{ .x = current.x + 1, .y = current.y },
                .{ .x = current.x - 1, .y = current.y },
                .{ .x = current.x, .y = current.y + 1 },
                .{ .x = current.x, .y = current.y - 1 },
            };

            const cur_val = map_get(map, current).? - '0';

            for (next) |n| {
                if (visited.contains(n))
                    continue;

                const next_val = map_get(map, n);
                if (next_val == null)
                    continue;

                if (next_val.? - '0' + 1 != cur_val)
                    continue;

                try queue.append(n);
            }
        }
    }

    //print_map_d(route_map);

    const starts = try find_from_map(map, '0', allocator);
    defer allocator.free(starts);

    var total: u32 = 0;
    for (starts) |start| {
        const routes = map_get(route_map, start).?;
        total += routes;
        //std.debug.print("{d}, {d}: {c} = {d}\n", .{ start.x, start.y, map_get(map, start).?, routes });
    }

    std.debug.print("{d}", .{total});
}
