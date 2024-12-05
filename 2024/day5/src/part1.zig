const std = @import("std");

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn is_right_order(rules: std.AutoHashMap(u32, std.ArrayList(u32)), page_list: []const u32) bool {
    for (page_list, 0..) |page, pos| {
        if (rules.get(page)) |later_pages| {
            for (later_pages.items) |later_page| {
                const later_pos = std.mem.indexOfScalar(u32, page_list, later_page);
                if (later_pos != null and later_pos.? < pos) {
                    return false;
                }
            }
        }
    }
    return true;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var rules = std.AutoHashMap(u32, std.ArrayList(u32)).init(allocator);
    var page_list_l = std.ArrayList([]u32).init(allocator);

    var rules_done = false;
    var lines = std.mem.splitSequence(u8, input, "\n");
    while (lines.next()) |line| {
        const line_trimmed = std.mem.trim(u8, line, " \n\r");
        if (line_trimmed.len == 0) {
            rules_done = true;
            continue;
        }

        if (!rules_done) {
            var parts = std.mem.tokenizeScalar(u8, line_trimmed, '|');
            const a = try std.fmt.parseInt(u32, parts.next().?, 10);
            const b = try std.fmt.parseInt(u32, parts.next().?, 10);
            if (rules.getPtr(a)) |*rule_list| {
                try rule_list.*.append(b);
            } else {
                var rule_list = std.ArrayList(u32).init(allocator);
                try rule_list.append(b);
                try rules.put(a, rule_list);
            }
        } else {
            var pages = std.mem.tokenizeScalar(u8, line_trimmed, ',');
            var p_list = std.ArrayList(u32).init(allocator);
            while (pages.next()) |page| {
                const num = try std.fmt.parseInt(u32, page, 10);
                try p_list.append(num);
            }
            try page_list_l.append(try p_list.toOwnedSlice());
        }
    }

    const page_list = try page_list_l.toOwnedSlice();

    var total: u32 = 0;
    for (page_list) |pages| {
        if (is_right_order(rules, pages)) {
            const mid_val = pages[pages.len / 2];
            total += mid_val;
        }
    }

    std.debug.print("{d}\n", .{total});
}
