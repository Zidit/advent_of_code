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
const Map = struct { data: []u8, h: usize, w: usize };

const neighbors = [_]Vec2{
    .{ .x = 0, .y = 1 },
    .{ .x = 0, .y = -1 },
    .{ .x = -1, .y = 0 },
    .{ .x = 1, .y = 0 },
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

fn copy_map(map: Map, allocator: std.mem.Allocator) !Map {
    const data = try allocator.alloc(u8, map.h * map.w);
    @memcpy(data, map.data);

    return .{ .data = data, .h = map.h, .w = map.w };
}

fn calc_area(map: Map, start_pos: Vec2, allocator: std.mem.Allocator) !struct { u32, u32 } {
    var queue = std.AutoArrayHashMap(Vec2, void).init(allocator);
    defer queue.deinit();
    try queue.put(start_pos, void{});

    var visited = std.AutoHashMap(Vec2, void).init(allocator);
    defer visited.deinit();

    const target_val = map_get(map, start_pos).?;
    var area: u32 = 0;

    while (queue.count() > 0) {
        const current = queue.pop().key;
        try visited.put(current, void{});
        area += 1;

        for (neighbors) |ne| {
            const n = ne.sum(current);
            if (visited.contains(n)) {
                continue;
            }

            const next_val = map_get(map, n);
            if (next_val == null or (next_val.? != target_val)) {
                continue;
            }

            try queue.put(n, void{});
        }
    }

    var it = visited.keyIterator();
    while (it.next()) |key| {
        map_set(map, key.*, '.');
    }

    var corners: u32 = 0;
    it = visited.keyIterator();
    while (it.next()) |key| {
        const pos = key.*;

        const up = visited.contains(pos.sum(neighbors[0]));
        const down = visited.contains(pos.sum(neighbors[1]));
        const left = visited.contains(pos.sum(neighbors[2]));
        const right = visited.contains(pos.sum(neighbors[3]));

        if ((!up and !right) or (up and right and !visited.contains(pos.sum(diagonals[0]))))
            corners += 1;

        if ((!right and !down) or (right and down and !visited.contains(pos.sum(diagonals[1]))))
            corners += 1;

        if ((!down and !left) or (down and left and !visited.contains(pos.sum(diagonals[2]))))
            corners += 1;

        if ((!left and !up) or (left and up and !visited.contains(pos.sum(diagonals[3]))))
            corners += 1;
    }

    return .{ area, corners };
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

    var total: u32 = 0;
    for (0..map.h) |y| {
        for (0..map.w) |x| {
            const vec: Vec2 = .{ .x = @intCast(x), .y = @intCast(y) };
            if (map_get(map, vec).? == '.') {
                continue;
            }
            const result = try calc_area(map, vec, allocator);
            total += result[0] * result[1];
        }
    }

    std.debug.print("{d}\n", .{total});
}
