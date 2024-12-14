const std = @import("std");

const Map = struct { data: []u8, h: usize, w: usize };

const Vec2 = struct {
    x: i32,
    y: i32,

    pub fn init(x: i32, y: i32) Vec2 {
        return .{ .x = x, .y = y };
    }

    pub fn init_u(x: u32, y: u32) Vec2 {
        return .{ .x = @intCast(x), .y = @intCast(y) };
    }

    pub fn add(self: Vec2, other: Vec2) Vec2 {
        return .{ .x = self.x + other.x, .y = self.y + other.y };
    }

    pub fn equal(self: Vec2, other: Vec2) bool {
        return self.x == other.x and self.y == other.y;
    }
};

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn split_srting(input: []const u8, delim: u8, allocator: std.mem.Allocator) ![][]const u8 {
    var arr = std.ArrayList([]const u8).init(allocator);
    defer arr.deinit();

    var parts = std.mem.splitScalar(u8, input, delim);
    while (parts.next()) |p| {
        try arr.append(p);
    }

    return arr.toOwnedSlice();
}

fn map_inc(map: Map, pos: Vec2) !void {
    if (pos.x < 0 or pos.y < 0 or pos.y >= map.h or pos.x >= map.w)
        return error.OutOfRange;

    const x: usize = @intCast(pos.x);
    const y: usize = @intCast(pos.y);
    map.data[y * map.w + x] += 1;
}

fn print_map_d(map: Map) void {
    for (0..map.h) |y| {
        const line = map.data[y * map.w .. (y + 1) * map.w];
        for (line) |value| {
            const v: u8 = if (value != 0) '#' else ' ';
            std.debug.print("{c}", .{v});
        }
        std.debug.print("\n", .{});
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

    const width = 101;
    const height = 103;

    var robots = std.ArrayList(struct { Vec2, Vec2 }).init(allocator);
    defer robots.deinit();

    var lines = std.mem.splitSequence(u8, input, "\n");
    while (lines.next()) |line| {
        const line_trim = std.mem.trim(u8, line, " \n\r");
        const pv = try split_srting(line_trim, ' ', allocator);

        const p = try split_srting((try split_srting(pv[0], '=', allocator))[1], ',', allocator);
        const pos = Vec2.init(try std.fmt.parseInt(i32, p[0], 10), try std.fmt.parseInt(i32, p[1], 10));

        const v = try split_srting((try split_srting(pv[1], '=', allocator))[1], ',', allocator);
        const vel = Vec2.init(try std.fmt.parseInt(i32, v[0], 10), try std.fmt.parseInt(i32, v[1], 10));

        try robots.append(.{ pos, vel });
    }

    const robot_count: i32 = @intCast(robots.items.len);

    var sec: u32 = 0;
    for (0..50000) |_| {
        var sum = Vec2.init(0, 0);

        for (robots.items) |*r| {
            const pos: Vec2 = r.*[0];
            const vel: Vec2 = r.*[1];

            var end = Vec2.init(pos.x + vel.x, pos.y + vel.y);
            end = Vec2.init(@rem(end.x, width), @rem(end.y, height));
            end = Vec2.init(if (end.x < 0) width + end.x else end.x, if (end.y < 0) height + end.y else end.y);
            r.*[0] = end;
            sum = sum.add(end);
        }

        const mean = Vec2.init(@divTrunc(sum.x, robot_count), @divTrunc(sum.y, robot_count));
        var variance = Vec2.init(0, 0);

        for (robots.items) |r| {
            const s = Vec2.init(try std.math.powi(i32, r[0].x - mean.x, 2), try std.math.powi(i32, r[0].y - mean.y, 2));
            variance = variance.add(s);
        }

        sec += 1;
        if (variance.x < 300000 and variance.y < 300000) {
            std.debug.print("{d} -> {any}\n", .{ sec, variance });
            break;
        }
    }

    const map_data = try allocator.alloc(u8, width * height);
    @memset(map_data, 0);
    const map: Map = .{ .data = map_data, .h = height, .w = width };
    defer allocator.free(map_data);

    for (robots.items) |r| {
        try map_inc(map, r[0]);
    }

    print_map_d(map);

    std.debug.print("{d}\n", .{sec});
}
