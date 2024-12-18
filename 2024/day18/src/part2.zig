const std = @import("std");

const Vec2 = struct {
    x: i32,
    y: i32,

    pub fn init(x: anytype, y: anytype) Vec2 {
        return .{ .x = @intCast(x), .y = @intCast(y) };
    }

    pub fn add(self: Vec2, other: Vec2) Vec2 {
        return .{ .x = self.x + other.x, .y = self.y + other.y };
    }

    pub fn equal(self: Vec2, other: Vec2) bool {
        return self.x == other.x and self.y == other.y;
    }
};
const Map = struct { data: []u8, h: usize, w: usize, allocator: std.mem.Allocator };

const neighbors = [_]Vec2{
    .{ .x = 0, .y = -1 }, //Up
    .{ .x = 1, .y = 0 }, //Right
    .{ .x = 0, .y = 1 }, //Down
    .{ .x = -1, .y = 0 }, //Left
};

const diagonals = [_]Vec2{
    .{ .x = 1, .y = 1 },
    .{ .x = 1, .y = -1 },
    .{ .x = -1, .y = -1 },
    .{ .x = -1, .y = 1 },
};

fn split_string(input: []const u8, delim: []const u8, allocator: std.mem.Allocator) ![][]const u8 {
    var arr = std.ArrayList([]const u8).init(allocator);
    defer arr.deinit();

    var parts = std.mem.splitSequence(u8, input, delim);
    while (parts.next()) |p| {
        try arr.append(p);
    }

    return arr.toOwnedSlice();
}

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

fn find_uniques_from_map(map: Map, allocator: std.mem.Allocator) std.AutoHashMap(u8, Vec2) {
    var results = std.AutoHashMap(u8, Vec2).init(allocator);

    for (0..map.h) |y| {
        const line = map.data[y * map.w .. (y + 1) * map.w];
        for (0..map.w) |x| {
            if (!results.contains(line[x])) {
                try results.put(line[x], .{ .x = x, .y = y });
            }
        }
    }

    return results;
}

fn data_to_map(input: []const u8, allocator: std.mem.Allocator) !Map {
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

    return .{ .data = try data.toOwnedSlice(), .h = height, .w = width, .allocator = allocator };
}

fn copy_map(map: Map, allocator: std.mem.Allocator) !Map {
    const data = try allocator.alloc(u8, map.h * map.w);
    @memcpy(data, map.data);

    return .{ .data = data, .h = map.h, .w = map.w, .allocator = allocator };
}

fn map_init(w: usize, h: usize, init_val: u8, allocator: std.mem.Allocator) !Map {
    const data = try allocator.alloc(u8, w * h);
    @memset(data, init_val);
    return .{ .data = data, .h = h, .w = w, .allocator = allocator };
}

fn map_init_walled(w: usize, h: usize, init_val: u8, wall_val: u8, allocator: std.mem.Allocator) !Map {
    const map = try map_init(w, h, init_val, allocator);

    for (0..map.h) |y| {
        map_set(map, Vec2.init(0, y), wall_val);
        map_set(map, Vec2.init(map.w - 1, y), wall_val);
    }

    for (0..map.w) |x| {
        map_set(map, Vec2.init(x, 0), wall_val);
        map_set(map, Vec2.init(x, map.h - 1), wall_val);
    }
    return map;
}

fn path(map: Map, start_pos: Vec2, end_pos: Vec2, allocator: std.mem.Allocator) !u32 {
    var queue = std.AutoArrayHashMap(Vec2, u32).init(allocator);
    defer queue.deinit();
    try queue.put(start_pos, 0);

    var visited = std.AutoHashMap(Vec2, struct { u32, Vec2 }).init(allocator);
    defer visited.deinit();

    while (queue.count() > 0) {
        const sort_context: struct {
            data: std.AutoArrayHashMap(Vec2, u32),
            pub fn lessThan(self: @This(), lhs: usize, rhs: usize) bool {
                const l = self.data.values()[lhs];
                const r = self.data.values()[rhs];
                return l > r;
            }
        } = .{ .data = queue };

        queue.sort(sort_context);
        const current = queue.pop();

        if (current.key.equal(end_pos)) {
            var tiles: u32 = 0;
            var parent = visited.get(current.key);
            while (parent != null and !parent.?[1].equal(start_pos)) {
                map_set(map, parent.?[1], 'x');
                parent = visited.get(parent.?[1]);
                tiles += 1;
            }

            return visited.get(current.key).?[0];
        }

        const next = [_]struct { Vec2, u32 }{
            .{ current.key.add(neighbors[0]), 1 },
            .{ current.key.add(neighbors[1]), 1 },
            .{ current.key.add(neighbors[2]), 1 },
            .{ current.key.add(neighbors[3]), 1 },
        };

        for (next) |n| {
            const pos = n[0];
            const cost = current.value + n[1];

            if (map_get(map, pos) == '#') {
                continue;
            }

            const big: u32 = std.math.maxInt(u32);
            if ((visited.get(n[0]) orelse .{ big, current.key })[0] < cost)
                continue;

            try visited.put(n[0], .{ cost, current.key });
            try queue.put(n[0], cost);
        }
    }
    return error.OutOfRange;
}

fn test_map(map: Map, walls: []Vec2, a: usize, b: usize) bool {
    const offset = Vec2.init(1, 1);
    for (walls[a..b]) |w| {
        map_set(map, w.add(offset), '#');
    }

    return path(map, Vec2.init(1, 1), Vec2.init(map.w - 2, map.h - 2), std.heap.page_allocator) != error.OutOfRange;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");
    const size = 71;

    var corruptions = std.ArrayList(Vec2).init(allocator);
    defer corruptions.deinit();

    var lines = std.mem.splitSequence(u8, input, "\n");
    while (lines.next()) |line| {
        const line_trimmed = std.mem.trim(u8, line, " \n\r");
        const values = try split_string(line_trimmed, ",", allocator);
        const x = try std.fmt.parseInt(i32, values[0], 10);
        const y = try std.fmt.parseInt(i32, values[1], 10);
        try corruptions.append(Vec2.init(x, y));
    }

    var a: usize = 0;
    var b: usize = corruptions.items.len - 1;

    while (b - a > 1) {
        const map: Map = try map_init_walled(size + 2, size + 2, '.', '#', allocator);
        const m = @divFloor((a + b), 2);

        //std.debug.print("{d} {d} ", .{ a, b });
        const result = test_map(map, corruptions.items, 0, m);
        //std.debug.print("{any}\n", .{result});
        //print_map(map);

        if (result) {
            a = m;
        } else {
            b = m;
        }
        allocator.free(map.data);
    }

    std.debug.print("{d},{d}\n", .{ corruptions.items[a].x, corruptions.items[a].y });
}
