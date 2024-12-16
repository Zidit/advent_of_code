const std = @import("std");

const Vec2 = struct {
    x: i32,
    y: i32,

    pub fn init(x: i32, y: i32) Vec2 {
        return .{ .x = x, .y = y };
    }

    pub fn init_u(x: u32, y: u32) Vec2 {
        return .{ .x = @intCast(x), .y = @intCast(y) };
    }

    pub fn sum(self: Vec2, other: Vec2) Vec2 {
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

const pd = struct {
    pos: Vec2,
    dir: usize,
};

fn print_path(map: Map, start: pd, end: Vec2, visited: anytype) void {
    var parent = visited.get(start);
    if (parent == null or parent.?[1].items[0].pos.equal(end))
        return;

    for (parent.?[1].items) |p| {
        map_set(map, p.pos, 'O');
        print_path(map, p, end, visited);
    }
}

fn path(map: Map, start_pos: Vec2, end_pos: Vec2, allocator: std.mem.Allocator) !u32 {
    var queue = std.AutoArrayHashMap(pd, u32).init(allocator);
    defer queue.deinit();
    try queue.put(.{ .pos = start_pos, .dir = 1 }, 0);

    var visited = std.AutoHashMap(pd, struct { u32, std.ArrayList(pd) }).init(allocator);
    defer visited.deinit();

    while (queue.count() > 0) {
        const sort_context: struct {
            data: std.AutoArrayHashMap(pd, u32),
            pub fn lessThan(self: @This(), lhs: usize, rhs: usize) bool {
                const l = self.data.values()[lhs];
                const r = self.data.values()[rhs];
                //std.debug.print("{any} {any}\n", .{ l, r });
                return l > r;
            }
        } = .{ .data = queue };

        queue.sort(sort_context);
        const current = queue.pop();

        if (current.key.pos.equal(end_pos)) {
            print_path(map, current.key, start_pos, visited);

            return visited.get(current.key).?[0];
        }

        const next = [_]struct { pd, u32 }{
            .{ .{ .pos = current.key.pos.sum(neighbors[current.key.dir]), .dir = current.key.dir }, 1 },
            .{ .{ .pos = current.key.pos, .dir = (current.key.dir + 1) % 4 }, 1000 },
            .{ .{ .pos = current.key.pos, .dir = (current.key.dir + 3) % 4 }, 1000 },
        };

        for (next) |n| {
            const pos = n[0].pos;
            const cost = current.value + n[1];

            if (map_get(map, pos) == '#') {
                continue;
            }

            const val = visited.get(n[0]);
            if (val != null and val.?[0] < cost)
                continue;

            if (val != null and val.?[0] == cost) {
                //std.debug.print("Collision: {any}\n", .{n[0]});
                const k = visited.getEntry(n[0]).?.value_ptr;
                try k.*[1].append(current.key);
                continue;
            }

            var pd_list = std.ArrayList(pd).init(allocator);
            try pd_list.append(current.key);
            try visited.put(n[0], .{ cost, pd_list });

            //try visited.put(n[0], .{ cost, t });
            try queue.put(n[0], cost);
        }
    }
    return error.OutOfRange;
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

    const start = (try find_from_map(map, 'S', allocator))[0];
    const end = (try find_from_map(map, 'E', allocator))[0];
    //std.debug.print("{any} {any}\n", .{ start, end });

    _ = try path(map, start, end, allocator);
    const total = std.mem.count(u8, map.data, "O") + 2;

    print_map(map);
    std.debug.print("{d}\n", .{total});
}
