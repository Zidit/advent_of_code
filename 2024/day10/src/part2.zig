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

fn map_inc(map: Map, pos: Vec2, val: u8) !void {
    if (pos.x < 0 or pos.y < 0 or pos.y >= map.h or pos.x >= map.w)
        return error.OutOfRange;

    const x: usize = @intCast(pos.x);
    const y: usize = @intCast(pos.y);
    map.data[y * map.w + x] += val;
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

const Node = struct { pos: Vec2, value: u32 };
fn lessThanFn(_: Node, lhs: Node, rhs: Node) bool {
    return lhs.value > rhs.value;
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

    const starts = try find_from_map(map, '0', allocator);
    defer allocator.free(starts);

    const route_map = .{ .data = try allocator.alloc(u8, map.h * map.w), .h = map.h, .w = map.w };
    defer allocator.free(route_map.data);

    var total: u32 = 0;
    for (starts) |start| {
        @memset(route_map.data, 0);
        try map_inc(route_map, start, 1);

        var visited = std.AutoHashMap(Vec2, u32).init(allocator);
        defer visited.deinit();

        var queue = std.ArrayList(Node).init(allocator);
        defer queue.deinit();

        try queue.append(.{ .pos = start, .value = 0 });

        while (queue.items.len > 0) {
            std.sort.insertion(Node, queue.items, queue.items[0], lessThanFn);
            const current = queue.pop().pos;

            if (visited.contains(current))
                continue;

            const cur_val = map_get(map, current).? - '0';
            try visited.put(current, cur_val);

            const next = [_]Vec2{
                .{ .x = current.x + 1, .y = current.y },
                .{ .x = current.x - 1, .y = current.y },
                .{ .x = current.x, .y = current.y + 1 },
                .{ .x = current.x, .y = current.y - 1 },
            };

            for (next) |n| {
                const next_val = map_get(map, n);
                if (next_val == null)
                    continue;

                if (next_val.? - '0' != cur_val + 1)
                    continue;

                if (map_get(route_map, current)) |value|
                    try map_inc(route_map, n, value);

                if (!visited.contains(n))
                    try queue.append(.{ .pos = n, .value = cur_val + 1 });
            }
        }

        const ends = try find_from_map(map, '9', allocator);
        defer allocator.free(ends);

        //print_map_d(route_map);

        var route_total: u32 = 0;
        for (ends) |end| {
            const routes = map_get(route_map, end).?;
            route_total += routes;
            //std.debug.print("{d}, {d}: {c} = {d}\n", .{ start.x, start.y, map_get(map, start).?, routes });
        }

        // std.debug.print("{d}\n", .{route_total});
        total += route_total;
    }

    std.debug.print("{d}", .{total});
}
